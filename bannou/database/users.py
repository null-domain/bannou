from __future__ import annotations

__all__: typing.Sequence[str] = ("User",)

import typing

import sqlalchemy
import sqlalchemy.dialects.postgresql as sqla_pg
from sqlalchemy import orm

from bannou.database import association_tables
from bannou.database import base

if typing.TYPE_CHECKING:
    import tanjun


class User(base.BaseMeta):
    __tablename__: str = "users"

    id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.BigInteger(), primary_key=True, autoincrement=False)

    @classmethod
    async def create(
        cls, id: int, /, session_maker: tanjun.injecting.Injected[base.AsyncSessionT], guild_id: int | None = None
    ) -> None:
        async with session_maker.begin() as session:
            await session.execute(
                sqla_pg.insert(cls).values(id=id).on_conflict_do_nothing()  # type: ignore[no-untyped-call]
            )
            if guild_id:
                await session.execute(
                    sqla_pg.insert(association_tables.UserGuild)  # type: ignore[no-untyped-call]
                    .values(user_id=id, guild_id=guild_id)
                    .on_conflict_do_nothing()
                )
