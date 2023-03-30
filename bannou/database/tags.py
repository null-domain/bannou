from __future__ import annotations

__all__: typing.Sequence[str] = ("Tag",)

import datetime
import typing

import sqlalchemy
from sqlalchemy import orm

from bannou.database import base


class Tag(base.BaseMeta):
    __tablename__ = "tags"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True, nullable=False)
    # TODO: created_by column mapping to an individual user via User model
    tag_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(length=32), nullable=False, unique=True)
    content: orm.Mapped[str] = orm.mapped_column(sqlalchemy.Text(), nullable=False)
    created_on: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy.func.now()
    )
    uses: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer(), nullable=False, server_default=sqlalchemy.text("'0'")
    )
