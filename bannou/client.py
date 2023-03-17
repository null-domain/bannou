import pathlib

import databases
import hikari
import tanjun

from bannou import settings
from bannou.database import context


def build_bot() -> hikari.GatewayBot:
    bot = hikari.GatewayBot(
        token=settings.bot_settings.bot_token.get_secret_value(),
        intents=hikari.Intents.ALL,
        logs=settings.bot_settings.logging,
    )

    (
        tanjun.Client.from_gateway_bot(bot, declare_global_commands=True)  # noqa - Pycharm dumb
        .load_directory(pathlib.Path(__file__).parent / "extensions")
        .set_type_dependency(databases.Database, context.BaseMeta.database)
    )

    return bot
