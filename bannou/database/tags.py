from __future__ import annotations

__all__: typing.Sequence[str] = ("Tag",)

import datetime
import typing

import sqlalchemy
from sqlalchemy import orm

from bannou.database import base

if typing.TYPE_CHECKING:
    from bannou.database.guilds import Guild
    from bannou.database.users import User


class Tag(base.BaseMeta):
    __tablename__: str = "tags"
    __table_args__: typing.Any = (sqlalchemy.UniqueConstraint("guild_id", "name"),)

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)

    user_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey("users.id"), nullable=False)
    user: orm.Mapped[User] = orm.relationship()

    guild_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey("guilds.id"), nullable=False)
    guild: orm.Mapped[Guild] = orm.relationship(back_populates="tags")

    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(length=32), nullable=False)
    content: orm.Mapped[str] = orm.mapped_column(sqlalchemy.Text(), nullable=False)
    created_on: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy.func.now()
    )
    uses: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer(), nullable=False, server_default="0")
    embeds_json: orm.Mapped[str] = orm.mapped_column(sqlalchemy.Text(), nullable=True)
