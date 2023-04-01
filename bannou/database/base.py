from __future__ import annotations

__all__: typing.Sequence[str] = ("Database", "DatabaseModel")

import abc
import typing
from contextlib import asynccontextmanager

import asyncpg
import hikari

if typing.TYPE_CHECKING:
    from bannou.settings import Secret
    from bannou.settings import Service


class Database:
    __slots__: typing.Sequence[str] = (
        "_service",
        "_user",
        "_password",
        "_host",
        "_port",
        "_pool",
        "_is_closed",
        "_name",
    )

    def __init__(self, app: hikari.GatewayBot, settings: Service) -> None:
        if settings.protocol != "postgresql":
            raise ValueError("Database protocol must be 'postgresql'")

        if not settings.user:
            raise ValueError("Database user must be specified")

        if not settings.password:
            raise ValueError("Database password must be specified")

        self._service = settings
        self._user = settings.user
        self._password = settings.password
        self._host = settings.host
        self._port = settings.port
        self._name = settings.path
        self._port = settings.port
        self._pool: asyncpg.Pool[asyncpg.Record] | None = None
        self._is_closed: bool = False

        DatabaseModel._db = self
        DatabaseModel._app = app

    @property
    def is_closed(self) -> bool:
        """Whether the database is closed."""
        return self._is_closed

    @property
    def user(self) -> str:
        """The username for the connection."""
        return self._user

    @property
    def password(self) -> Secret:
        """The password for the connection."""
        return self._password

    @property
    def host(self) -> str:
        """The hostname for the connection."""
        return self._host

    @property
    def port(self) -> int:
        """The port for the connection. By default, this is 5432."""
        return self._port

    @property
    def name(self) -> str:
        """The name of the database."""
        return self._name

    @property
    def pool(self) -> asyncpg.Pool[asyncpg.Record]:
        """The underlying connection pool for the database."""
        if self._pool is None:
            raise ValueError("Database pool is not initialized")
        return self._pool

    @property
    def dsn(self) -> str:
        """The DSN for the database."""
        return self._service.build_url()

    async def connect(self) -> None:
        if self._is_closed:
            raise hikari.ComponentStateConflictError("Database is already closed")
        self._pool = await asyncpg.create_pool(dsn=self.dsn)

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
        self._is_closed = True

    @asynccontextmanager
    async def acquire(self) -> typing.AsyncIterator[asyncpg.Connection[asyncpg.Record]]:
        con: asyncpg.Connection = await self.pool.acquire()  # type: ignore
        try:
            yield con
        finally:
            await self.pool.release(con)  # type: ignore

    async def execute(self, query: str, *args: typing.Any, timeout: float | None = None) -> str:
        return await self.pool.execute(query, *args, timeout=timeout)

    async def fetch(self, query: str, *args: typing.Any, timeout: float | None = None) -> list[asyncpg.Record]:
        return await self.pool.fetch(query, *args, timeout=timeout)

    async def fetchrow(self, query: str, *args: typing.Any, timeout: float | None = None) -> asyncpg.Record | None:
        return await self.pool.fetchrow(query, *args, timeout=timeout)

    async def fetchval(self, query: str, *args: typing.Any, timeout: float | None = None) -> typing.Any:
        return await self.pool.fetchval(query, *args, timeout=timeout)


class DatabaseModel(abc.ABC):
    __slots__: typing.Sequence[str] = ("_db", "_app")

    _db: Database
    _app: hikari.GatewayBot

    @abc.abstractmethod
    def from_record(self, record: asyncpg.Record) -> DatabaseModel:
        """Build a model from a database record."""
