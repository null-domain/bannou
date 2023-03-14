from bannou import client, settings

try:
    import uvloop

    uvloop.install()
except ImportError:
    print("uvloop is not installed, falling back to asyncio")

bot_settings = settings.BotSettings("config.yaml")
bot = client.build_bot(bot_settings)

bot.run()
