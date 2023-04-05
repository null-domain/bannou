from __future__ import annotations

__all__: typing.Sequence[str] = ("Tag",)

import datetime
import typing

import sqlalchemy
from sqlalchemy import orm

from bannou.database import base

if typing.TYPE_CHECKING:
    from bannou.database.guilds import Guild


class Tag(base.BaseMeta):
    __tablename__: str = "tags"
    __table_args__: typing.Any = (sqlalchemy.UniqueConstraint("guild_id", "tag_name"),)

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True, nullable=False)
    # TODO: created_by column mapping to an individual user via User model
    guild_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey("guilds.id"))
    guild: orm.Mapped[Guild] = orm.relationship(back_populates="tags")
    tag_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(length=32), nullable=False)
    content: orm.Mapped[str] = orm.mapped_column(sqlalchemy.Text(), nullable=False)
    created_on: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy.func.now()
    )
    uses: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer(), nullable=False, server_default=sqlalchemy.text("'0'")
    )
