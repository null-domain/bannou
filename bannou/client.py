import pathlib


from databases import Database as DatabaseType
import hikari
import tanjun

from bannou.settings import BotSettings
from bannou.database.context import BaseMeta


def build_bot(settings: BotSettings) -> hikari.GatewayBot:
    bot = hikari.GatewayBot(
        token=settings.bot_token.get_secret_value(),
        intents=hikari.Intents.ALL,
        logs=settings.logging,
    )

    (
        tanjun.Client.from_gateway_bot(bot, declare_global_commands=True)  # noqa - Pycharm dumb
        .load_directory(pathlib.Path(__file__).parent / "extensions")
        .set_type_dependency(BotSettings, settings)
        .set_type_dependency(DatabaseType, BaseMeta.database)
    )

    return bot
