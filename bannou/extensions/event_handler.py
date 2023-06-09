from __future__ import annotations

import logging
import urllib.parse

import hikari
import sqlalchemy.dialects.postgresql as sql_pg
import tanjun
from sqlalchemy.ext import asyncio as sqlalchemy_async

from bannou import database

component = tanjun.Component(name=__name__)


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


@component.with_listener()
async def on_guild_create(
    event: hikari.events.GuildAvailableEvent | hikari.events.GuildJoinEvent,
    session_maker: tanjun.injecting.Injected[database.base.AsyncSessionT],
) -> None:
    async with session_maker.begin() as session:
        await session.execute(
            sql_pg.insert(database.Guild)  # type: ignore[no-untyped-call]
            .values(id=event.guild_id)
            .on_conflict_do_nothing()
        )


@tanjun.as_loader()
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component)


@tanjun.as_unloader()
def unload(client: tanjun.abc.Client) -> None:
    client.remove_component(component)
