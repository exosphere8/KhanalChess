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
            "INSERT INTO users (display_name) VALUES ('logout test') "
            "RETURNING id"
        ).fetchone()
    yield row[0]
    with migrate.connect() as conn:
        conn.execute("DELETE FROM users WHERE id = %s", (row[0],))


def test_logout_without_cookie_is_fine():
    response = client.post("/logout")
    assert response.status_code == 204


def test_logout_with_unknown_cookie_is_fine():
    response = client.post("/logout", headers=cookie("not-a-real-session"))
    assert response.status_code == 204


def test_logout_ends_the_session(user_id):
    token = sessions.create(user_id, timedelta(hours=1))
    assert sessions.lookup(token) == user_id
    response = client.post("/logout", headers=cookie(token))
    assert response.status_code == 204
    assert sessions.lookup(token) is None
    assert client.get("/me", headers=cookie(token)).status_code == 401


def test_logout_tells_the_browser_to_drop_the_cookie():
    response = client.post("/logout")
    header = response.headers["set-cookie"]
    assert header.startswith(f"{COOKIE_NAME}=")
    assert "Max-Age=0" in header
