import os

import psycopg


def connect_args() -> dict:
    """Return connection settings: DATABASE_URL if set, else the POSTGRES_ ones."""
    url = os.environ.get("DATABASE_URL")
    if url:
        return {"conninfo": url}
    return {
        "host": os.environ.get("POSTGRES_HOST", "db"),
        "dbname": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }


def db_available() -> bool:
    """Return True if PostgreSQL answers a trivial query."""
    try:
        with psycopg.connect(**connect_args(), connect_timeout=3) as conn:
            conn.execute("SELECT 1")
        return True
    except (KeyError, psycopg.Error):
        return False
