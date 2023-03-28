from __future__ import annotations

__all__: typing.Sequence[str] = ("Tag",)

import datetime
import typing

import sqlalchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from bannou.database import base


class Tag(base.BaseMeta):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: created_by column mapping to an individual user via User model
    tag_name: Mapped[str] = mapped_column(sqlalchemy.String(length=32), nullable=False)
    content: Mapped[str] = mapped_column(sqlalchemy.Text(), nullable=False)
    created_on: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy.func.now()
    )
    uses: Mapped[int] = mapped_column(sqlalchemy.Integer(), nullable=False, server_default=sqlalchemy.text("'0'"))
