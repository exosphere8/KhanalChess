import os

import psycopg
import pytest

from backend import migrate, users

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


@pytest.fixture(autouse=True)
def clean_test_users():
    """Remove users made with the fake provider, before and after."""

    def clean():
        with migrate.connect() as conn:
            conn.execute(
                "DELETE FROM users WHERE id IN "
                "(SELECT user_id FROM identities WHERE provider = 'test')"
            )

    clean()
    yield
    clean()


def test_new_identity_creates_a_user():
    user_id = users.find_or_create("test", "sub-1", "ann@example.com", "Ann")
    assert users.get(user_id) == {"id": user_id, "display_name": "Ann"}
    with migrate.connect() as conn:
        row = conn.execute(
            "SELECT email FROM identities WHERE user_id = %s", (user_id,)
        ).fetchone()
    assert row[0] == "ann@example.com"


def test_same_identity_gives_the_same_user():
    first = users.find_or_create("test", "sub-2", "bob@example.com", "Bob")
    second = users.find_or_create("test", "sub-2", "bob@example.com", "Bobby")
    assert second == first
    assert users.get(first)["display_name"] == "Bob"
    with migrate.connect() as conn:
        count = conn.execute(
            "SELECT count(*) FROM identities "
            "WHERE provider = 'test' AND provider_user_id = 'sub-2'"
        ).fetchone()[0]
    assert count == 1
