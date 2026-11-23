"""Read and create users."""

from backend.migrate import connect


def get(user_id: int) -> dict | None:
    """Return the user's id and display name, or None."""
    with connect() as conn:
        row = conn.execute(
            "SELECT id, display_name FROM users WHERE id = %s",
            (user_id,),
        ).fetchone()
    return {"id": row[0], "display_name": row[1]} if row else None


def find_or_create(
    provider: str, provider_user_id: str, email: str, display_name: str
) -> int:
    """Return the user id for this identity, creating the user if new."""
    with connect() as conn:
        with conn.transaction():
            row = conn.execute(
                "SELECT user_id FROM identities"
                " WHERE provider = %s AND provider_user_id = %s",
                (provider, provider_user_id),
            ).fetchone()
            if row:
                return row[0]
            user_id = conn.execute(
                "INSERT INTO users (display_name) VALUES (%s) RETURNING id",
                (display_name,),
            ).fetchone()[0]
            conn.execute(
                "INSERT INTO identities"
                " (user_id, provider, provider_user_id, email)"
                " VALUES (%s, %s, %s, %s)",
                (user_id, provider, provider_user_id, email),
            )
    return user_id
