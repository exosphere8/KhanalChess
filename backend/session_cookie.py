"""Set and clear the sign-in cookie on a response."""

import os
from datetime import timedelta

from fastapi import Response

COOKIE_NAME = "kc_session"
LIFETIME = timedelta(days=7)
STATE_COOKIE_NAME = "kc_oauth_state"
STATE_LIFETIME = timedelta(minutes=10)
STATE_PATH = "/auth/google"


def _secure() -> bool:
    """Secure cookies are on unless COOKIE_SECURE=false (local http only)."""
    return os.environ.get("COOKIE_SECURE", "true").lower() != "false"


def set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=int(LIFETIME.total_seconds()),
        path="/",
        secure=_secure(),
        httponly=True,
        samesite="lax",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        secure=_secure(),
        httponly=True,
        samesite="lax",
    )


def set_state_cookie(response: Response, state: str) -> None:
    """Keep the sign-in state number for 10 minutes, for /auth/google only."""
    response.set_cookie(
        key=STATE_COOKIE_NAME,
        value=state,
        max_age=int(STATE_LIFETIME.total_seconds()),
        path=STATE_PATH,
        secure=_secure(),
        httponly=True,
        samesite="lax",
    )


def clear_state_cookie(response: Response) -> None:
    response.delete_cookie(
        key=STATE_COOKIE_NAME,
        path=STATE_PATH,
        secure=_secure(),
        httponly=True,
        samesite="lax",
    )
