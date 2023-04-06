from __future__ import annotations

__all__: typing.Sequence[str] = ("User",)

import typing

import sqlalchemy
from sqlalchemy import orm

from bannou.database import base

if typing.TYPE_CHECKING:
    from bannou.database.guilds import Guild


class User(base.BaseMeta):
    __tablename__: str = "users"
    __table_args__: typing.Any = (sqlalchemy.PrimaryKeyConstraint("id", "guild_id"),)

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.BigInteger())
    guild_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey("guilds.id"))
    guild: orm.Mapped[Guild] = orm.relationship(back_populates="users")
