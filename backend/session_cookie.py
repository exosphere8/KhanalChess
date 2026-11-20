"""Set and clear the sign-in cookie on a response."""

from datetime import timedelta

from fastapi import Response

COOKIE_NAME = "kc_session"
LIFETIME = timedelta(days=7)


def set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=int(LIFETIME.total_seconds()),
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )
