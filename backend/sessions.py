"""Create, look up and delete sign-in sessions."""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from backend.migrate import connect


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create(user_id: int, lifetime: timedelta) -> str:
    """Store a new session and return the random value for the cookie."""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(UTC) + lifetime
    with connect() as conn:
        conn.execute(
            "INSERT INTO sessions (token_hash, user_id, expires_at) "
            "VALUES (%s, %s, %s)",
            (_hash(token), user_id, expires_at),
        )
    return token


def lookup(token: str) -> int | None:
    """Return the user id of a live session, or None."""
    with connect() as conn:
        row = conn.execute(
            "SELECT user_id FROM sessions "
            "WHERE token_hash = %s AND expires_at > now()",
            (_hash(token),),
        ).fetchone()
    return row[0] if row else None


def delete(token: str) -> None:
    """Remove a session, which logs that browser out."""
    with connect() as conn:
        conn.execute(
            "DELETE FROM sessions WHERE token_hash = %s",
            (_hash(token),),
        )
