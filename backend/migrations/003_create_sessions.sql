-- 003: one row per signed-in browser. token_hash is a one-way hash of the
-- random value kept in the cookie, so a copy of this table cannot be used
-- to sign in. Deleting the row logs that browser out.
CREATE TABLE sessions (
    token_hash text PRIMARY KEY,
    user_id    bigint NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    created_at timestamptz NOT NULL DEFAULT now(),
    expires_at timestamptz NOT NULL
);

CREATE INDEX sessions_user_id_idx ON sessions (user_id);
