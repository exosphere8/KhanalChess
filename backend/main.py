from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.db import db_available
from backend.game import validate_move

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
