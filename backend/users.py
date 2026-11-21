"""Read users."""

from backend.migrate import connect


def get(user_id: int) -> dict | None:
    """Return the user's id and display name, or None."""
    with connect() as conn:
        row = conn.execute(
            "SELECT id, display_name FROM users WHERE id = %s",
            (user_id,),
        ).fetchone()
    return {"id": row[0], "display_name": row[1]} if row else None
