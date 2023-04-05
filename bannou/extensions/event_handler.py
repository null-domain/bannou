from __future__ import annotations

import logging
import urllib.parse

import hikari
import sqlalchemy
import tanjun
from sqlalchemy.ext import asyncio as sqlalchemy_async

from bannou import database as db

component = tanjun.Component(name=__name__)


async def pre_execution_hook(
    ctx: tanjun.abc.Context, session_maker: tanjun.injecting.Injected[db.base.AsyncSession]
) -> None:
    if ctx.guild_id is not None:
        try:
            async with session_maker.begin() as session:
                session.add(db.guilds.Guild(id=ctx.guild_id))
        except sqlalchemy.exc.IntegrityError:
            pass  # Guild already exists in DB


@component.with_client_callback(tanjun.ClientCallbackNames.STARTING)
async def startup_events(bot: tanjun.injecting.Injected[hikari.GatewayBot]) -> None:
    application = await bot.rest.fetch_application()
    install_parameters = application.install_parameters

    url = f"https://discord.com/oauth2/authorize?client_id={application.id}"

    if install_parameters:
        url += f"&permissions={int(install_parameters.permissions)}&scope={' '.join(install_parameters.scopes)}"

    logging.getLogger("bannou").info(f"Invite url: {urllib.parse.quote(url, safe=':/?=&')}")


@component.with_client_callback(tanjun.ClientCallbackNames.CLOSED)
async def shutdown_events(db_engine: tanjun.injecting.Injected[sqlalchemy_async.AsyncEngine]) -> None:
    await db_engine.dispose()


loader = component.make_loader()
