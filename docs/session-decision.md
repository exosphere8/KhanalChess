# Session decision record

Status: proposed. Date: 2026-11-18, updated 2026-11-20. The cookie settings
and the session lifetime are chosen; only the cleanup of expired rows is
still open; see Not decided.

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
6. The cookie is named kc_session and is set with HttpOnly, Secure,
   SameSite=Lax, Path=/ and no Domain. HttpOnly and Secure are on: the owner
   confirmed them on Nov 21. Lax sends the cookie when a person
   arrives from a link on another site, so they do not look signed out.
7. The session lifetime is fixed: 7 days from sign-in, with no renewal. The
   cookie has Max-Age of 7 days, the same as the server end time.

## Reasons

- The server can end a session at any time by deleting its row.
- A leaked copy of the table does not let anyone sign in.
- The lifetime is a parameter, so changing it later is a small change.

## Trade-offs

- Every request that needs a signed-in user reads the database.
- Expired rows are ignored but never deleted, so they pile up until a
  cleanup job exists.
- A fixed lifetime means even an active person signs in again after 7 days.
- Max-Age saves the cookie on the computer's disk for up to 7 days. OWASP
  advises leaving it out; we accept the cost for a login that lasts days.

## Not decided

- When expired rows are cleaned up.
- Whether a sliding lifetime is wanted later.

## Not checked

- The 7 days is our own choice, not an OWASP number. The OWASP Session
  Management Cheat Sheet itself was not read in full; timeouts were read
  through MDN and OWASP's other pages.
- Whether SameSite=Lax causes trouble on the return from Google sign-in.
- Whether the __Host- name prefix works on http://localhost. It was left out
  for now.
- The Session B note on HttpOnly and Secure was not re-checked.

## Out of scope

Linking providers, remember-me, a list of a user's sessions, account
deletion.
