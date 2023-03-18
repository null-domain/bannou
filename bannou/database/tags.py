from __future__ import annotations

__all__: typing.Sequence[str] = ("Tag",)

import typing

import ormar
import sqlalchemy

from bannou.database import base

if typing.TYPE_CHECKING:
    import datetime


class Tag(ormar.Model):
    class Meta(base.BaseMeta):
        tablename = "tags"

    id: int = ormar.Integer(primary_key=True)
    # TODO: created_by column mapping to an individual user via User model
    created_on: datetime.datetime = ormar.DateTime(nullable=True, server_default=sqlalchemy.func.now())
    tag_name: str = ormar.String(max_length=32, nullable=False)
    uses: int = ormar.Integer(default=0, nullable=False)
    content: str = ormar.String(max_length=4000, nullable=False)
