from fastapi.testclient import TestClient

from backend import main

client = TestClient(main.app)


def test_health_db_ok(monkeypatch):
    monkeypatch.setattr(main, "db_available", lambda: True)
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_db_unavailable(monkeypatch):
    monkeypatch.setattr(main, "db_available", lambda: False)
    response = client.get("/health/db")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}
