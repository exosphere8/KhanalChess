from fastapi import Response

from backend.session_cookie import (
    clear_session_cookie,
    set_session_cookie,
)


def test_set_cookie_has_the_agreed_rules():
    response = Response()
    set_session_cookie(response, "abc")
    header = response.headers["set-cookie"].lower()
    assert "kc_session=abc" in header
    assert "httponly" in header
    assert "secure" in header
    assert "samesite=lax" in header
    assert "path=/" in header
    assert "max-age=604800" in header
    assert "domain" not in header


def test_clear_cookie_expires_it_now():
    response = Response()
    clear_session_cookie(response)
    header = response.headers["set-cookie"].lower()
    assert "kc_session" in header
    assert "max-age=0" in header
