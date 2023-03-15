import logging
import urllib.parse

import alluka
import hikari
import tanjun

from databases import Database

component = tanjun.Component(name=__name__)


@component.with_client_callback(tanjun.ClientCallbackNames.STARTING)
async def startup_events(bot: alluka.Injected[hikari.GatewayBot], database: alluka.Injected[Database]) -> None:
    await database.connect()

    application = await bot.rest.fetch_application()
    install_parameters = application.install_parameters

    url = f"https://discord.com/oauth2/authorize?client_id={application.id}"

    if install_parameters:
        url += f"&permissions={int(install_parameters.permissions)}&scope={' '.join(install_parameters.scopes)}"

    logging.getLogger("bannou").info(f"Invite url: {urllib.parse.quote(url, safe=':/?=&')}")


@component.with_client_callback(tanjun.ClientCallbackNames.CLOSED)
async def shutdown_events(bot: alluka.Injected[hikari.GatewayBot], database: alluka.Injected[Database]) -> None:
    await database.disconnect()


loader = component.make_loader()
