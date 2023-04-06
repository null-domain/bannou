from __future__ import annotations

__all__: typing.Sequence[str] = ("Guild",)

import typing

import sqlalchemy
from sqlalchemy import orm

from bannou.database import base

if typing.TYPE_CHECKING:
    from bannou.database.tags import Tag
    from bannou.database.users import User


class Guild(base.BaseMeta):
    __tablename__: str = "guilds"

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.BigInteger(), primary_key=True)

    tags: orm.Mapped[list[Tag]] = orm.relationship(back_populates="guild")
    users: orm.Mapped[list[User]] = orm.relationship(back_populates="guild")
