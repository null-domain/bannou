import sqlalchemy
from databases import Database
from ormar import ModelMeta

from bannou import settings


# TODO: Use already-instantiated bot settings (see PR 9)
class BaseMeta(ModelMeta):
    database = Database(settings.BotSettings("config.yaml").postgres.build_url())
    metadata = sqlalchemy.MetaData()
