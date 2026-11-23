# Auth decision record

Status: accepted with the Google sign-in endpoints. Date: 2026-11-16.
Google's OpenID Connect page has been read; see Not checked.

## Context

Visitors must have an account in our database before they can play. A guest
who presses PLAY sees the sign-up menu. A signed-in user sees Log Out and
About Us. There are not enough users yet for a leaderboard, so the home page
stays a single centred column and the leaderboard comes later.

## Options

Sign in with a provider (OAuth), starting with Google
- We never store passwords.
- More providers (GitHub, Meta, X) can be added later.

Email and password
- Nothing external to set up.
- We would have to hash passwords and handle resets ourselves.

## Decision (accepted)

1. First version: sign in with Google only.
2. Two tables. users has one row per person. identities has one row per
   sign-in method: the provider name, the provider's user id, and a link to
   the user. Adding a provider later adds rows, not columns.
3. One person can link several providers to one account.
4. Build order, one PR each: this record, database tables and migrations,
   sign-up and login endpoints with tests, the frontend sign-up screen, then
   PLAY gated behind sign-in.
5. Sign-in state: a random number kept in a 10-minute HttpOnly cookie
   (kc_oauth_state, path /auth/google), compared with the value Google
   sends back. No extra table.
6. A customer is found by the provider name and Google's sub value, never
   by email. A new customer gets a users row and an identities row in one
   transaction. display_name is Google's name, or the part of the email
   before the @ if no name is sent.
7. The kc_session cookie is set after a good return. Secure is on unless
   COOKIE_SECURE=false is set for local http.

## Reasons

- Not storing passwords removes the riskiest part of a first account system.
- The identities table makes a new provider a small change.

## Trade-offs

- Users without a Google account cannot play until another provider is added.
- We depend on Google being available and keeping its terms.
- The same person signing in with two providers can end up with two accounts
  unless we link them on purpose.
- The free Render database expires (see docs/cd-decision.md). It must be
  replaced before real users sign up, because accounts are stored data.

## Not checked

Google: only the OpenID Connect page was read in full. Not read: the
redirect URI page, the scopes page, the Data Access page. The scopes sent
(openid email profile) were chosen in code and are not confirmed there.
Whether nonce is needed is not decided. A real sign-in in a browser has
not been tried yet.

GitHub, Meta and X: sign-in requirements not checked. To be read from the
providers' own pages before each provider is built.

## Out of scope

Leaderboard, password reset, account deletion, game history.
