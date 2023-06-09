from __future__ import annotations

import pathlib

import hikari
import orjson
import tanjun
from sqlalchemy.ext import asyncio as sqlalchemy_async

from bannou import database
from bannou import settings


def build_bot() -> hikari.GatewayBot:
    bot = hikari.GatewayBot(
        token=settings.BOT_SETTINGS.bot_token.get_secret_value(),
        intents=hikari.Intents.ALL,
        logs=settings.BOT_SETTINGS.logging,
    )

    engine = sqlalchemy_async.create_async_engine(
        settings.BOT_SETTINGS.postgres.build_url(),
        echo=False,
        json_serializer=orjson.dumps,
        json_deserializer=orjson.loads,
    )

    (
        tanjun.Client.from_gateway_bot(bot, declare_global_commands=True)
        .load_directory(pathlib.Path(__file__).parent / "extensions")
        .set_type_dependency(tanjun.AnyHooks, tanjun.AnyHooks())
        .set_type_dependency(
            database.base.AsyncSessionT,
            sqlalchemy_async.async_sessionmaker(engine, expire_on_commit=False),
        )
        .set_type_dependency(sqlalchemy_async.AsyncEngine, engine)
    )

    return bot
