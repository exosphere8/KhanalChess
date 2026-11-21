from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend import sessions, users
from backend.db import db_available
from backend.game import validate_move
from backend.session_cookie import COOKIE_NAME

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
