import sqlalchemy
from databases import Database
from ormar import ModelMeta

from bannou import bot_settings

class BaseMeta(ModelMeta):
    database = Database(bot_settings.postgres.build_url())
    metadata = sqlalchemy.MetaData()
