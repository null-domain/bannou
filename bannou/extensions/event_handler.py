from __future__ import annotations

import logging
import urllib.parse

import hikari
import tanjun

from bannou.database import base

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
async def shutdown_events(database: tanjun.injecting.Injected[base.Database]) -> None:
    await database.close()


loader = component.make_loader()
