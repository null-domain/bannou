from __future__ import annotations

import sqlalchemy.orm


class BaseMeta(sqlalchemy.orm.DeclarativeBase):
    pass
