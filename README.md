# KhanalChess

A minimalist chess web app with a bishop as its logo. It is my final-year
computer engineering project, built to learn DevOps and clean code from end
to end.

Started on November 11, 2026, as a personal challenge: take an idea from my
head to a deployed product, one small reviewed change at a time.

## What works today

- Move validation: POST /move checks a move with python-chess, behind a
  Pydantic model.
- Health checks: GET /health, and GET /health/db, which answers 503 when
  PostgreSQL is unreachable.
- Database: users, identities and sessions tables, created by a small
  migration runner (numbered SQL files, each applied once).
- Sessions: helpers to create, look up and delete a session (only a hash of
  the cookie value is stored), and helpers to set and clear the cookie
  (Secure, HttpOnly, SameSite=Lax, 7 days).
- Who am I: GET /me answers with the id and display name of the signed-in
  user, or 401. POST /logout ends the session and always answers 204.
- Frontend: a React opening menu with an original SVG bishop. The buttons are
  placeholders for now.
- Images: the API and the frontend are published to GitHub Container Registry
  after every merge to main.

Not built yet: Google sign-in (nothing hands out the session cookie yet), the
game screen, deployment.

## Stack

- Backend: Python 3.13, FastAPI, python-chess, PostgreSQL 17 (psycopg 3, no
  ORM)
- Frontend: React, Vite, Vitest, ESLint
- DevOps: Docker, Docker Compose, GitHub Actions, GHCR, Dependabot, gitleaks
- Planned: Terraform and Kubernetes. Deployment to Render, then AWS, is
  parked.

## The pipeline

Every pull request runs five checks in GitHub Actions:

- test: pytest against a real PostgreSQL service, including the migrations
- lint: ruff on the whole repository
- docker: builds the API image, starts it and smoke tests /health
- frontend: install, dependency audit, lint, tests and build
- gitleaks: scans for committed secrets

A sixth job, publish, runs only after a merge to main. It pushes both images
tagged with the commit hash, and moves latest.

The main branch is protected: a pull request is required, only squash merges
are allowed, force pushes are blocked, the branch must be up to date, and
all five checks must pass.

## How I work

- One small pull request per change, one branch each, conventional commit
  messages. Squash merges make the history read like a changelog.
- Gates are proven by failing on purpose. PRs #13, #16 and #26 broke a test,
  the linter and the smoke test deliberately, were never merged, and stay
  closed as evidence that the gates block a bad change.
- Verify, do not assume. Before merging the database PR I read the CI log to
  confirm the new tests really ran against PostgreSQL, because a green mark
  can hide skipped tests. In CI a missing database fails the tests instead of
  skipping them.
- Supply chain care: exact version pins for React, Vite and its plugin,
  Dependabot with a 14-day cooldown, a dependency audit in CI, and gitleaks.
- A major dependency bump gets its release notes read and its tests run
  locally before the merge.
- Decisions are written down before they are built (see below).

## Decisions

- docs/cd-decision.md: deploy to Render first to get a working pipeline,
  then move to AWS with Terraform.
- docs/auth-decision.md: sign in with Google first. Separate users and
  identities tables mean a new provider adds rows, not columns.
- docs/session-decision.md: sessions kept in the database, with a cookie
  named kc_session (Secure, HttpOnly, SameSite=Lax, 7 days, no renewal).
- docs/typescript-decision.md: finish the backend first, then switch the
  frontend to TypeScript in one pull request.

The first three records are still marked proposed. The TypeScript record is
decided.

## Run it locally

You need Python 3.13, Docker Desktop and Node (CI uses Node 24).

Backend tests and lint, from the repo root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
ruff check .
```

The database tests skip when no database is reachable, so a plain pytest
run stays green on a laptop.

API and database:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Change POSTGRES_PASSWORD in .env first. The API answers on localhost:8000.
Create the tables with the migration runner. It runs inside the api
container, because the database publishes no port to the host:

```powershell
docker compose run --rm --build api python -m backend.migrate
```

Frontend:

```powershell
cd frontend
npm ci
npm run dev
```

The dev server runs at localhost:5173. Use npm run lint, npm test and
npm run build for the other checks.

## Roadmap

1. Google sign-in in the backend (sessions, /me and log out are done).
2. Switch the frontend to TypeScript, in one pull request.
3. Frontend: PLAY opens a guest sign-up menu with a Google button, then a
   signed-in menu.
4. The frontend as a service in Docker Compose.
5. Deployment: Render first, then AWS with Terraform.
6. A leaderboard, once there are enough players.

## License

MIT
