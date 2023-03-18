from __future__ import annotations

from typing import TYPE_CHECKING

import ormar
import sqlalchemy

from bannou.database.models import BaseMeta

if TYPE_CHECKING:
    import datetime


class Tag(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tags"

    id: int = ormar.Integer(primary_key=True)
    # TODO: created_by column mapping to an individual user via User model
    created_on: datetime.datetime = ormar.DateTime(nullable=False, server_default=sqlalchemy.func.now())
    tag_name: str = ormar.String(max_length=32, nullable=False)
    uses: int = ormar.Integer(default=0, nullable=False)
    content: str = ormar.String(max_length=4000, nullable=False)
