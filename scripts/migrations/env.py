import asyncio
from logging.config import fileConfig

from alembic import context as alembic_context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

import bannou.database.context as bannou_context

# we import the models even though they aren't used directly
# otherwise alembic will not detect them
from bannou.database import models  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = alembic_context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add the model's MetaData object here
target_metadata = bannou_context.BaseMeta.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

config.set_main_option("sqlalchemy.url", str(bannou_context.BaseMeta.database.url))


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


def do_run_migrations(connection: Connection) -> None:
    alembic_context.configure(connection=connection, target_metadata=target_metadata)

    with alembic_context.begin_transaction():
        alembic_context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
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
