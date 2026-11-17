import os
from datetime import timedelta

import psycopg
import pytest

from backend import migrate, sessions

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


@pytest.fixture
def user_id():
    """A throwaway user. Deleting it also removes its sessions."""
    with migrate.connect() as conn:
        row = conn.execute(
            "INSERT INTO users (display_name) VALUES ('session test') "
            "RETURNING id"
        ).fetchone()
    yield row[0]
    with migrate.connect() as conn:
        conn.execute("DELETE FROM users WHERE id = %s", (row[0],))


def test_created_session_can_be_looked_up(user_id):
    token = sessions.create(user_id, timedelta(hours=1))
    assert sessions.lookup(token) == user_id


def test_table_keeps_a_hash_not_the_cookie_value(user_id):
    token = sessions.create(user_id, timedelta(hours=1))
    with migrate.connect() as conn:
        rows = conn.execute(
            "SELECT token_hash FROM sessions WHERE user_id = %s",
            (user_id,),
        ).fetchall()
    assert [row[0] for row in rows] == [sessions._hash(token)]
    assert token not in rows[0][0]


def test_unknown_value_finds_nobody():
    assert sessions.lookup("not-a-real-session") is None


def test_expired_session_finds_nobody(user_id):
    token = sessions.create(user_id, timedelta(seconds=-1))
    assert sessions.lookup(token) is None


def test_delete_logs_the_browser_out(user_id):
    token = sessions.create(user_id, timedelta(hours=1))
    sessions.delete(token)
    assert sessions.lookup(token) is None


def test_deleting_the_user_removes_the_session(user_id):
    token = sessions.create(user_id, timedelta(hours=1))
    with migrate.connect() as conn:
        conn.execute("DELETE FROM users WHERE id = %s", (user_id,))
    assert sessions.lookup(token) is None
