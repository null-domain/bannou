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

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.BigInteger(), primary_key=True, autoincrement=False)
