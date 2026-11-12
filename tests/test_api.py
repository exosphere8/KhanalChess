from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_move_legal():
    response = client.post("/move", json={"fen": START_FEN, "move": "e2e4"})
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert "fen" in body


def test_move_illegal():
    response = client.post("/move", json={"fen": START_FEN, "move": "e2e5"})
    assert response.status_code == 200
    assert response.json()["valid"] is False


def test_move_missing_field_returns_422():
    response = client.post("/move", json={"fen": START_FEN})
    assert response.status_code == 422


def test_move_oversized_input_returns_422():
    response = client.post("/move", json={"fen": "x" * 101, "move": "e2e4"})
    assert response.status_code == 422
