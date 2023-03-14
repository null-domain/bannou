import tanjun

component = tanjun.Component(name=__name__)


@tanjun.with_str_slash_option("yourmom", "testing")
@tanjun.as_slash_command("ping", "See the bots ping!")
async def ping(ctx: tanjun.abc.SlashContext, yourmom: str) -> None:
    await ctx.respond(f"Pong! {yourmom}")


component.load_from_scope()
loader = component.make_loader()
