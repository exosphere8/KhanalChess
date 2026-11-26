"""Tests for the database connection settings (no database needed)."""

import pytest

from backend.db import connect_args


def test_database_url_wins(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@example:5432/kc")
    monkeypatch.setenv("POSTGRES_DB", "ignored")
    assert connect_args() == {"conninfo": "postgresql://u:p@example:5432/kc"}


def test_postgres_settings_without_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("POSTGRES_HOST", "localhost")
    monkeypatch.setenv("POSTGRES_DB", "kc")
    monkeypatch.setenv("POSTGRES_USER", "kc_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "kc_pass")
    assert connect_args() == {
        "host": "localhost",
        "dbname": "kc",
        "user": "kc_user",
        "password": "kc_pass",
    }


def test_missing_setting_raises(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    with pytest.raises(KeyError):
        connect_args()
