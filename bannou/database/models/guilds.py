from __future__ import annotations

import asyncpg
import attr
import hikari

from bannou.database.base import DatabaseModel


@attr.define(weakref_slot=False)
class Guild(DatabaseModel):
    id: hikari.Snowflakeish = attr.field(on_setattr=attr.setters.frozen)

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> Guild:
        return cls(
            id=record["guild_id"],
        )

    @classmethod
    async def fetch(cls, guild: hikari.SnowflakeishOr[hikari.PartialGuild]) -> Guild | None:
        """Fetch a guild from the database.

        Parameters
        ----------
        guild : hikari.SnowflakeishOr[hikari.PartialGuild]
            The guild to fetch.

        Returns
        -------
        Guild | None
            The guild if it exists in database, otherwise None.
        """
        query = "SELECT * FROM guilds WHERE guild_id = $1"
        record = await cls._db.fetchrow(query, int(guild))
        return cls.from_record(record) if record else None

    @classmethod
    async def create(
        cls,
        guild: hikari.SnowflakeishOr[hikari.PartialGuild],
    ) -> Guild:
        """Create a new guild in the database.

        Parameters
        ----------
        guild : hikari.SnowflakeishOr[hikari.PartialGuild]
            The guild to create.

        Raises
        ------
        ValueError
            If a tag already exists with the same name for the guild.
        """

        query = "INSERT INTO guilds (guild_id) VALUES ($1)"
        try:
            await cls._db.execute(query, int(guild))
        except asyncpg.UniqueViolationError:
            raise ValueError(f"Guild '{int(guild)}' already exists in database.")
        return cls(int(guild))

    async def save(self) -> None:
        """Save the current state of the Guild instance to the database.
        If the guild already exists, overwrite it."""

        query = "INSERT INTO guilds (guild_id) VALUES ($1) ON CONFLICT (guild_id) DO NOTHING"
        await self._db.execute(query, int(self.id))
