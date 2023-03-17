from bannou import client, settings

try:
    import uvloop

    uvloop.install()
except ImportError:
    print("uvloop is not installed, falling back to asyncio")

bot = client.build_bot(settings.BotSettings("config.yaml"))

bot.run()
