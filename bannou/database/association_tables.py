from __future__ import annotations

__all__: typing.Sequence[str] = ("UserGuild",)

import typing

import sqlalchemy
from sqlalchemy import orm

from bannou.database import base

if typing.TYPE_CHECKING:
    from bannou.database.guilds import Guild
    from bannou.database.users import User


class UserGuild(base.BaseMeta):
    __tablename__: str = "users_guilds"

    user_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey("users.id"), primary_key=True)
    user: orm.Mapped[User] = orm.relationship()
    guild_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey("guilds.id"), primary_key=True)
    guild: orm.Mapped[Guild] = orm.relationship(back_populates="users")
