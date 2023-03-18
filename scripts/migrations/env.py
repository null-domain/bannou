from __future__ import annotations

import asyncio
import pathlib
import runpy
from logging.config import fileConfig

import sqlalchemy
from alembic import context as alembic_context
from sqlalchemy import engine as sqlachademy_engine
from sqlalchemy import pool as sqlachademy_pool
from sqlalchemy.ext import asyncio as sqlachademy_asyncio

from bannou import database as bannou_database
from bannou.database import base as bannou_models_base

# Detect and import module objects
models_modules_path = pathlib.Path(bannou_database.__file__).parent

for models_module_path in models_modules_path.iterdir():
    if models_module_path.suffix != ".py" and models_modules_path.name != "__init__":
        continue

    runpy.run_path(str(models_module_path))

# Define variables to use bellow
config = alembic_context.config
target_metadata = bannou_models_base.BaseMeta.metadata

# Init logging
if config.config_file_name:
    fileConfig(config.config_file_name)


# Set defaults
config.set_main_option("sqlalchemy.url", str(bannou_models_base.BaseMeta.database.url))


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


def do_run_migrations(connection: sqlachademy_engine.Connection) -> None:
    alembic_context.configure(connection=connection, target_metadata=target_metadata)

    with alembic_context.begin_transaction():
        alembic_context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = sqlachademy_asyncio.AsyncEngine(
        sqlalchemy.engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=sqlachademy_pool.NullPool,
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
