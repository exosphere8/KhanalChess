"""Apply the numbered SQL files in backend/migrations, once each."""

import os
import sys
from pathlib import Path

import psycopg

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def connect() -> psycopg.Connection:
    return psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "db"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=3,
        autocommit=True,
    )


def run() -> list[str]:
    """Apply every new migration file in order; return the names applied."""
    applied_now = []
    with connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "name text PRIMARY KEY, "
            "applied_at timestamptz NOT NULL DEFAULT now())"
        )
        rows = conn.execute("SELECT name FROM schema_migrations").fetchall()
        already = {row[0] for row in rows}
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name in already:
                continue
            with conn.transaction():
                conn.execute(path.read_text(encoding="utf-8"))
                conn.execute(
                    "INSERT INTO schema_migrations (name) VALUES (%s)",
                    (path.name,),
                )
            applied_now.append(path.name)
    return applied_now


def main() -> int:
    try:
        applied = run()
    except KeyError as missing:
        print(f"Missing environment variable: {missing}")
        return 1
    except psycopg.Error as error:
        print(f"Database error: {error}")
        return 1
    for name in applied:
        print(f"applied {name}")
    if not applied:
        print("nothing to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
