"""Talk to Google: build the sign-in address, and swap the slip."""

import base64
import json
import os
from urllib.parse import urlencode

import httpx2

REDIRECT_URI = "http://localhost:8000/auth/google/callback"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


class GoogleError(Exception):
    """Google did not give us a usable answer."""


def login_url(state: str) -> str:
    """The address that sends the customer to Google's ID office."""
    query = urlencode(
        {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": REDIRECT_URI,
            "state": state,
        }
    )
    return f"{AUTH_URL}?{query}"


def get_identity(code: str) -> dict:
    """Swap the one-time slip for who the customer is.

    The ID token comes straight from Google over HTTPS, after we showed
    our secret key, so we read it without checking its signature.
    """
    response = httpx2.post(
        TOKEN_URL,
        data={
            "code": code,
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    if response.status_code != 200:
        raise GoogleError(f"Google answered {response.status_code}")
    id_token = response.json().get("id_token")
    if not id_token:
        raise GoogleError("Google sent no ID token")
    payload = id_token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    claims = json.loads(base64.urlsafe_b64decode(payload))
    email = claims["email"]
    return {
        "sub": claims["sub"],
        "email": email,
        "display_name": claims.get("name") or email.split("@")[0],
    }
