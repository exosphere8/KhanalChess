# CD decision record

Status: proposed. Date checked: 2026-11-15. Facts come from the providers'
own pages unless marked otherwise.

## Context

KhanalChess is a FastAPI container image that talks to PostgreSQL. CI builds,
tests and lints it. CD must publish the image, run it at a public HTTPS
address, and smoke test /health and /health/db.

## Options

Render (free web service and free Postgres)
- Web service spins down after 15 minutes without traffic and needs about
  one minute to start again.
- 750 free instance hours per workspace per calendar month.
- Filesystem is ephemeral: files are lost on redeploy or restart.
- Free Postgres expires 30 days after creation, with a 14-day grace period
  before deletion. 1 GB, one per workspace, no backups, no pooling.
- Card rule at sign-up: not confirmed, to be checked when signing up.

AWS Free plan (account created about 2026-11-10, plan type to be confirmed
in the Billing console)
- Credits of about $100, plus up to $100 for setup activities.
- The Free plan closes the account after 6 months or when credits run out.
  AWS keeps the data for 90 days.
- App Runner reported closed to new customers (third-party source, not
  confirmed on AWS pages).

Google Cloud Run and Oracle Cloud Always Free
- Not re-verified on 2026-11-15. Both ask for a card at sign-up, and a
  prepaid virtual card may be rejected. Details stay out until checked.

## Decision (proposed)

1. Deploy to Render first, to get a working pipeline: build and push the
   image from GitHub Actions, deploy, smoke test.
2. Move the infrastructure to AWS in the Terraform stage and keep it as code.

## Reasons

- Render is free and needs no server administration, so the first CD run
  tests the pipeline rather than the infrastructure.
- The AWS Free plan has a hard end date, so it suits learning, not the
  permanent public address.

## Trade-offs

- The first request after idle is slow, so the smoke test needs a retry
  with a timeout.
- The free database expires. Since #60 it stores users, identities and
  sessions, so each expiry deletes every account. This is acceptable only
  while the Google app is in Testing and the project account is the only
  user. Move the database before publishing the Google app.
- Two platforms mean two deployments to maintain for a while.
- The image tested in CI and the image published are two builds of the same
  source. Building once and pushing that image would close the gap.
- :latest moves with every publish. Deploy from the :<sha> tag.

## Progress (2026-11-15)

- Done: CI publishes the image to GHCR after the three checks pass, only on a
  push to main, with the tags :<sha> and :latest (PR #24). The package is
  public. The pulled image answered /health with 200.
- Done: the docker job starts the built image and calls /health with a retry
  and a 60 s timeout (PR #25). Seen passing on main (CI #28) and failing on
  purpose in a throwaway PR (#26, closed, not merged).
- Not done: the Render service is not created (the card is expected to be
  active on 2026-11-18), no deploy job, no smoke test against a live host.
- Not started: AWS (plan type, MFA and budget alert still to be done).

## Out of scope

Domain name, Terraform, Kubernetes, scaling, a database that persists data.
