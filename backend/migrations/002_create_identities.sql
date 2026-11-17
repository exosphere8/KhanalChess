-- 002: one row per sign-in method. A person can have several.
CREATE TABLE identities (
    id               bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id          bigint NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    provider         text NOT NULL,
    provider_user_id text NOT NULL,
    email            text,
    created_at       timestamptz NOT NULL DEFAULT now(),
    UNIQUE (provider, provider_user_id)
);

CREATE INDEX identities_user_id_idx ON identities (user_id);
