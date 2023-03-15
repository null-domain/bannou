import sqlalchemy
from databases import Database
from ormar import ModelMeta

from bannou import bot_settings

_database = Database(bot_settings.postgres.build_url())
_metadata = sqlalchemy.MetaData()


class BaseMeta(ModelMeta):
    database = _database
    metadata = _metadata
