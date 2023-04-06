from __future__ import annotations

import asyncio
import pathlib
import runpy
from logging.config import fileConfig

import sqlalchemy
from alembic import context as alembic_context
from sqlalchemy import engine as sqlalchemy_engine
from sqlalchemy import pool as sqlalchemy_pool
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from bannou import settings as bannou_settings
from bannou.database import base as bannou_database

# Define variables to use bellow
config = alembic_context.config
target_metadata = bannou_database.BaseMeta.metadata

# Init logging
if config.config_file_name:
    fileConfig(config.config_file_name)


# Set defaults
config.set_main_option("sqlalchemy.url", bannou_settings.BOT_SETTINGS.postgres.build_url())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    alembic_context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with alembic_context.begin_transaction():
        alembic_context.run_migrations()


def do_run_migrations(connection: sqlalchemy_engine.Connection) -> None:
    alembic_context.configure(connection=connection, target_metadata=target_metadata)

    with alembic_context.begin_transaction():
        alembic_context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = sqlalchemy_asyncio.AsyncEngine(
        sqlalchemy.engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=sqlalchemy_pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if alembic_context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
