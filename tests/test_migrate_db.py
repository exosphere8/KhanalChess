import os

import psycopg
import pytest

from backend import migrate

pytestmark = pytest.mark.usefixtures("migrated")


@pytest.fixture(scope="module")
def migrated():
    """Run the migrations once against a real database."""
    try:
        migrate.run()
    except (KeyError, psycopg.Error) as error:
        if os.environ.get("CI"):
            pytest.fail(f"CI must provide a database: {error!r}")
        pytest.skip(f"no database reachable: {error!r}")


def _recorded() -> set[str]:
    with migrate.connect() as conn:
        rows = conn.execute("SELECT name FROM schema_migrations").fetchall()
    return {row[0] for row in rows}


def test_tables_exist():
    with migrate.connect() as conn:
        rows = conn.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public'"
        ).fetchall()
    tables = {row[0] for row in rows}
    assert {"users", "identities", "schema_migrations"} <= tables


def test_every_file_is_recorded():
    files = {path.name for path in migrate.MIGRATIONS_DIR.glob("*.sql")}
    assert files <= _recorded()


def test_second_run_applies_nothing():
    assert migrate.run() == []
