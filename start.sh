#!/bin/sh
# Start the API. On a real server, set RUN_MIGRATIONS=1 to apply
# new database migrations first. A failed migration stops the start.
set -e

if [ "$RUN_MIGRATIONS" = "1" ]; then
    python -m backend.migrate
fi

exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
