from __future__ import annotations

import asyncpg
import attr
import hikari

from bannou.database.base import DatabaseModel


@attr.define()
class Tag(DatabaseModel):
    guild_id: hikari.Snowflake
    name: str
    owner_id: hikari.Snowflake
    content: str
    uses: int = 0

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> Tag:
        return cls(
            guild_id=record["guild_id"],
            name=record["tag_name"],
            owner_id=record["owner_id"],
            content=record["content"],
            uses=record["uses"],
        )

    @classmethod
    async def fetch(cls, guild: hikari.SnowflakeishOr[hikari.PartialGuild], name: str) -> Tag | None:
        """Fetch a tag from the database.

        Parameters
        ----------
        guild: `hikari.SnowflakeishOr[hikari.PartialGuild]`
            The guild the tag belongs to.
        name: `str`
            The name of the tag.

        Returns
        -------
        Tag | None
            The tag if it exists, otherwise None.
        """
        query = "SELECT * FROM tags WHERE guild_id = $1 AND tag_name = $2"
        record = await cls._db.fetchrow(query, hikari.Snowflake(guild), name)
        return cls.from_record(record) if record else None

    @classmethod
    async def fetch_all(cls, guild: hikari.SnowflakeishOr[hikari.PartialGuild]) -> list[Tag]:
        """Fetch all tags that belong to a guild.

        Parameters
        ----------
        guild: `hikari.SnowflakeishOr[hikari.PartialGuild]`
            The guild to fetch tags for.
        """
        query = "SELECT * FROM tags WHERE guild_id = $1"
        records = await cls._db.fetch(query, hikari.Snowflake(guild))
        return [cls.from_record(record) for record in records]

    @classmethod
    async def create(
        cls,
        guild: hikari.SnowflakeishOr[hikari.PartialGuild],
        name: str,
        owner: hikari.SnowflakeishOr[hikari.PartialUser],
        content: str,
    ) -> Tag:
        """Create a new tag in the database.

        Parameters
        ----------
        guild: `hikari.SnowflakeishOr[hikari.PartialGuild]`
            The guild the tag is being created in.
        name: `str`
            The name of the tag.
        owner: `hikari.SnowflakeishOr[hikari.PartialUser]`
            The user who created the tag.
        content: `str`
            The content of the tag.

        Raises
        ------
        ValueError
            If a tag already exists with the same name for the guild.
        """

        query = "INSERT INTO tags (guild_id, tag_name, owner_id, content) VALUES ($1, $2, $3, $4)"
        try:
            await cls._db.execute(query, hikari.Snowflake(guild), name, hikari.Snowflake(owner), content)
        except asyncpg.UniqueViolationError:
            raise ValueError(f"Tag '{name}' already exists for guild '{hikari.Snowflake(guild)}'.")
        return cls(hikari.Snowflake(guild), name, hikari.Snowflake(owner), content)

    async def save(self) -> None:
        """Save the current state of the tag instance to the database.
        If a tag already exists, overwrite it."""

        query = """INSERT INTO tags (guild_id, tag_name, owner_id, content, uses) VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (guild_id, tag_name) DO UPDATE SET owner_id = $3, content = $4, uses = $5"""
        await self._db.execute(query, self.guild_id, self.name, self.owner_id, self.content, self.uses)