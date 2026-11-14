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
- The free database expires. This is acceptable while the app only checks
  the connection and stores no data.
- Two platforms mean two deployments to maintain for a while.

## Out of scope

Domain name, Terraform, Kubernetes, scaling, a database that persists data.
