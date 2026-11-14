import os

import psycopg


def db_available() -> bool:
    """Return True if PostgreSQL answers a trivial query."""
    try:
        with psycopg.connect(
            host=os.environ.get("POSTGRES_HOST", "db"),
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            connect_timeout=3,
        ) as conn:
            conn.execute("SELECT 1")
        return True
    except (KeyError, psycopg.Error):
        return False
