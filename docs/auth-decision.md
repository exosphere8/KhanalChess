# Auth decision record

Status: proposed. Date: 2026-11-16. Nothing about the providers has been
checked against their own pages yet; see Not checked.

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

## Decision (proposed)

1. First version: sign in with Google only.
2. Two tables. users has one row per person. identities has one row per
   sign-in method: the provider name, the provider's user id, and a link to
   the user. Adding a provider later adds rows, not columns.
3. One person can link several providers to one account.
4. Build order, one PR each: this record, database tables and migrations,
   sign-up and login endpoints with tests, the frontend sign-up screen, then
   PLAY gated behind sign-in.

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

Google's setup steps and requirements, and the sign-in requirements for
GitHub, Meta and X. To be read from the providers' own pages before each
provider is built.

## Out of scope

Leaderboard, password reset, account deletion, game history.
