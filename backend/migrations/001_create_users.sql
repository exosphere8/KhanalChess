-- 001: one row per person.
CREATE TABLE users (
    id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    display_name text,
    created_at   timestamptz NOT NULL DEFAULT now()
);
