from __future__ import annotations

import tanjun

component = tanjun.Component(name=__name__)


@tanjun.as_slash_command("ping", "See the bots ping!")
async def ping(ctx: tanjun.abc.SlashContext) -> None:
    await ctx.respond("Pong!")


component.load_from_scope()
loader = component.make_loader()
