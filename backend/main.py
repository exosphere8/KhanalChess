from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.game import validate_move

app = FastAPI(title="KhanalChess")


class MoveRequest(BaseModel):
    fen: str = Field(max_length=100)
    move: str = Field(max_length=5)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/move")
def move(request: MoveRequest):
    return validate_move(request.fen, request.move)
