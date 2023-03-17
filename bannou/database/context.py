import sqlalchemy
from databases import Database
from ormar import ModelMeta

from bannou import settings


class BaseMeta(ModelMeta):
    database = Database(settings.bot_settings.postgres.build_url())
    metadata = sqlalchemy.MetaData()
