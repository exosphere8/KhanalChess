import os
import re
from urllib.parse import parse_qs, urlparse

import psycopg
import pytest
from fastapi.testclient import TestClient

from backend import google_auth, migrate
from backend.main import app
from backend.session_cookie import COOKIE_NAME, STATE_COOKIE_NAME

pytestmark = pytest.mark.usefixtures("migrated")

client = TestClient(app)

SUB = "test-sub-callback"


def cookie(**cookies):
    """Send cookies by hand, so the test does not depend on how the
    client treats a Secure cookie over plain http."""
    return {"Cookie": "; ".join(f"{k}={v}" for k, v in cookies.items())}


@pytest.fixture(scope="module")
def migrated():
    """Run the migrations once against a real database."""
    try:
        migrate.run()
    except (KeyError, psycopg.Error) as error:
        if os.environ.get("CI"):
            pytest.fail(f"CI must provide a database: {error!r}")
        pytest.skip(f"no database reachable: {error!r}")


@pytest.fixture(autouse=True)
def clean_google_test_user():
    """Remove the fake Google customer, before and after."""

    def clean():
        with migrate.connect() as conn:
            conn.execute(
                "DELETE FROM users WHERE id IN (SELECT user_id FROM "
                "identities WHERE provider = 'google' "
                "AND provider_user_id = %s)",
                (SUB,),
            )

    clean()
    yield
    clean()


def fake_identity(code):
    return {"sub": SUB, "email": "gia@example.com", "display_name": "Gia"}


def must_not_be_called(code):
    raise AssertionError("Google must not be called")


def test_login_sends_the_customer_to_google(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "test-client-id")
    response = client.get("/auth/google/login", follow_redirects=False)
    assert response.status_code == 302
    location = response.headers["location"]
    assert location.startswith(google_auth.AUTH_URL)
    query = parse_qs(urlparse(location).query)
    assert query["client_id"] == ["test-client-id"]
    assert query["redirect_uri"] == [google_auth.REDIRECT_URI]
    state = query["state"][0]
    set_cookie = response.headers["set-cookie"]
    assert f"{STATE_COOKIE_NAME}={state}" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "Path=/auth/google" in set_cookie
    assert "Max-Age=600" in set_cookie


def test_callback_without_the_state_note_is_refused(monkeypatch):
    monkeypatch.setattr(google_auth, "get_identity", must_not_be_called)
    response = client.get(
        "/auth/google/callback?code=abc&state=xyz", follow_redirects=False
    )
    assert response.status_code == 400


def test_callback_with_a_different_state_is_refused(monkeypatch):
    monkeypatch.setattr(google_auth, "get_identity", must_not_be_called)
    response = client.get(
        "/auth/google/callback?code=abc&state=two",
        headers=cookie(**{STATE_COOKIE_NAME: "one"}),
        follow_redirects=False,
    )
    assert response.status_code == 400
    assert COOKIE_NAME not in response.headers.get("set-cookie", "")


def test_good_return_makes_a_ticket(monkeypatch):
    monkeypatch.setattr(google_auth, "get_identity", fake_identity)
    response = client.get(
        "/auth/google/callback?code=abc&state=s1",
        headers=cookie(**{STATE_COOKIE_NAME: "s1"}),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:5173/"
    set_cookie = response.headers["set-cookie"]
    assert "Max-Age=0" in set_cookie
    match = re.search(rf"{COOKIE_NAME}=([^;]+);", set_cookie)
    assert match
    me = client.get("/me", headers=cookie(**{COOKIE_NAME: match.group(1)}))
    assert me.status_code == 200
    assert me.json()["display_name"] == "Gia"


def test_google_failure_gives_no_ticket(monkeypatch):
    def broken(code):
        raise google_auth.GoogleError("boom")

    monkeypatch.setattr(google_auth, "get_identity", broken)
    response = client.get(
        "/auth/google/callback?code=abc&state=s1",
        headers=cookie(**{STATE_COOKIE_NAME: "s1"}),
        follow_redirects=False,
    )
    assert response.status_code == 502
    assert COOKIE_NAME not in response.headers.get("set-cookie", "")
