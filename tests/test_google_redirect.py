"""Tests for the Google return address setting (no database needed)."""

from urllib.parse import parse_qs, urlparse

from backend import google_auth


def test_default_is_localhost(monkeypatch):
    monkeypatch.delenv("GOOGLE_REDIRECT_URI", raising=False)
    assert google_auth.redirect_uri() == google_auth.DEFAULT_REDIRECT_URI


def test_setting_wins(monkeypatch):
    live = "https://example.onrender.com/auth/google/callback"
    monkeypatch.setenv("GOOGLE_REDIRECT_URI", live)
    assert google_auth.redirect_uri() == live


def test_login_url_uses_the_setting(monkeypatch):
    live = "https://example.onrender.com/auth/google/callback"
    monkeypatch.setenv("GOOGLE_REDIRECT_URI", live)
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "test-client-id")
    query = parse_qs(urlparse(google_auth.login_url("s")).query)
    assert query["redirect_uri"] == [live]
