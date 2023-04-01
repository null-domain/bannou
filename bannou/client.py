from __future__ import annotations

import pathlib

import hikari
import tanjun

from bannou import settings
from bannou.database import base


def build_bot() -> hikari.GatewayBot:
    bot = hikari.GatewayBot(
        token=settings.BOT_SETTINGS.bot_token.get_secret_value(),
        intents=hikari.Intents.ALL,
        logs=settings.BOT_SETTINGS.logging,
    )

    (
        tanjun.Client.from_gateway_bot(bot, declare_global_commands=True)
        .load_directory(pathlib.Path(__file__).parent / "extensions")
        .set_type_dependency(base.Database, base.Database(bot, settings.BOT_SETTINGS.postgres))
    )

    return bot
