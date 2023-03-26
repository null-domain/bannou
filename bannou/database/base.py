from __future__ import annotations

import sqlalchemy
from databases import Database
from ormar import ModelMeta

from bannou import settings

DATABASE = Database(settings.BOT_SETTINGS.postgres.build_url())
METADATA = sqlalchemy.MetaData()


class BaseMeta(ModelMeta):
    database = DATABASE
    metadata = METADATA
