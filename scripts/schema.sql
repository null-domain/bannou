CREATE TABLE IF NOT EXISTS schema_version (
    schema_ver INTEGER NOT NULL,
    inserted_at TIMESTAMPTZ,
    PRIMARY KEY(schema_ver)
);

CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT NOT NULL,
    PRIMARY KEY(guild_id)
);

CREATE TABLE IF NOT EXISTS tags (
    tag_name TEXT NOT NULL,
    guild_id BIGINT NOT NULL,
    tag_content TEXT NOT NULL,
    owner_id BIGINT NOT NULL, /* this should be a fk to a user */
    created_at TIMESTAMPTZ NOT NULL,
    uses INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY(tag_name, guild_id),
    FOREIGN KEY(guild_id) REFERENCES guilds(guild_id)
);
