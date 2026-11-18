# Session decision record

Status: proposed. Date: 2026-11-18. The cookie settings and the session
lifetime are still open; see Not decided.

## Context

After Google sign-in, the server must remember who is signed in. The
sessions table (migration 003, #44) and the helpers in backend/sessions.py
(#45) already exist. No endpoint uses them yet.

## Decision (proposed)

1. Sessions are stored in our own database, one row per signed-in browser.
2. The browser keeps a random value in a cookie (32 random bytes, made with
   secrets.token_urlsafe). The table keeps only its SHA-256 hash, so a copy
   of the table cannot be used to sign in.
3. A session has an end time (expires_at). lookup ignores expired sessions.
   create takes the lifetime as an argument; it does not choose one.
4. Logging out deletes the row.
5. Deleting a user also deletes their sessions (ON DELETE CASCADE).

## Reasons

- The server can end a session at any time by deleting its row.
- A leaked copy of the table does not let anyone sign in.
- The lifetime is a parameter, so changing it later is a small change.

## Trade-offs

- Every request that needs a signed-in user reads the database.
- Expired rows are ignored but never deleted, so they pile up until a
  cleanup job exists.

## Not decided

- The session lifetime: fixed or sliding, and how many days.
- The cookie settings (HttpOnly, Secure, SameSite, name, path).
- When expired rows are cleaned up.

## Not checked

What each cookie setting does in browsers. To be read from a reliable
source before the settings are chosen.

## Out of scope

Linking providers, remember-me, a list of a user's sessions, account
deletion.
