import os
import secrets

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from backend import google_auth, sessions, users
from backend.db import db_available
from backend.game import validate_move
from backend.session_cookie import (
    COOKIE_NAME,
    LIFETIME,
    STATE_COOKIE_NAME,
    clear_session_cookie,
    clear_state_cookie,
    set_session_cookie,
    set_state_cookie,
)

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

app = FastAPI(title="KhanalChess")


class MoveRequest(BaseModel):
    fen: str = Field(max_length=100)
    move: str = Field(max_length=5)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    if db_available():
        return {"status": "ok"}
    return JSONResponse(status_code=503, content={"status": "unavailable"})


@app.post("/move")
def move(request: MoveRequest):
    return validate_move(request.fen, request.move)


@app.get("/me")
def me(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    user_id = sessions.lookup(token) if token else None
    user = users.get(user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(status_code=401, detail="please sign in first")
    return user


@app.post("/logout", status_code=204)
def logout(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if token:
        sessions.delete(token)
    response = Response(status_code=204)
    clear_session_cookie(response)
    return response


@app.get("/auth/google/login")
def google_login():
    state = secrets.token_urlsafe(32)
    response = RedirectResponse(google_auth.login_url(state), status_code=302)
    set_state_cookie(response, state)
    return response


@app.get("/auth/google/callback")
def google_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
):
    expected = request.cookies.get(STATE_COOKIE_NAME)
    if not code or not state or not expected:
        raise HTTPException(status_code=400, detail="sign-in failed")
    if not secrets.compare_digest(state.encode(), expected.encode()):
        raise HTTPException(status_code=400, detail="sign-in failed")
    try:
        identity = google_auth.get_identity(code)
    except google_auth.GoogleError:
        raise HTTPException(status_code=502, detail="Google sign-in failed") from None
    user_id = users.find_or_create(
        "google",
        identity["sub"],
        identity["email"],
        identity["display_name"],
    )
    token = sessions.create(user_id, LIFETIME)
    response = RedirectResponse(f"{FRONTEND_URL}/", status_code=302)
    set_session_cookie(response, token)
    clear_state_cookie(response)
    return response
