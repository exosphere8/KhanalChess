import os
from datetime import timedelta

import psycopg
import pytest
from fastapi.testclient import TestClient

from backend import migrate, sessions
from backend.main import app
from backend.session_cookie import COOKIE_NAME

pytestmark = pytest.mark.usefixtures("migrated")

client = TestClient(app)


def cookie(token):
    """Send the cookie by hand, so the test does not depend on how the
    client treats a Secure cookie over plain http."""
    return {"Cookie": f"{COOKIE_NAME}={token}"}


@pytest.fixture(scope="module")
def migrated():
    """Run the migrations once against a real database."""
    try:
        migrate.run()
    except (KeyError, psycopg.Error) as error:
        if os.environ.get("CI"):
            pytest.fail(f"CI must provide a database: {error!r}")
        pytest.skip(f"no database reachable: {error!r}")


@pytest.fixture
def user_id():
    """A throwaway user. Deleting it also removes its sessions."""
    with migrate.connect() as conn:
        row = conn.execute(
            "INSERT INTO users (display_name) VALUES ('me test') "
            "RETURNING id"
        ).fetchone()
    yield row[0]
    with migrate.connect() as conn:
        conn.execute("DELETE FROM users WHERE id = %s", (row[0],))


def test_no_cookie_is_refused():
    response = client.get("/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "please sign in first"}


def test_unknown_cookie_is_refused():
    response = client.get("/me", headers=cookie("not-a-real-session"))
    assert response.status_code == 401


def test_expired_session_is_refused(user_id):
    token = sessions.create(user_id, timedelta(seconds=-1))
    response = client.get("/me", headers=cookie(token))
    assert response.status_code == 401


def test_live_session_says_who_is_signed_in(user_id):
    token = sessions.create(user_id, timedelta(hours=1))
    response = client.get("/me", headers=cookie(token))
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "display_name": "me test"}
