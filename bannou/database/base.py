from __future__ import annotations

import sqlalchemy.ext.asyncio
import sqlalchemy.orm

AsyncSessionT = sqlalchemy.ext.asyncio.async_sessionmaker[sqlalchemy.ext.asyncio.AsyncSession]


class BaseMeta(sqlalchemy.orm.DeclarativeBase):
    pass
