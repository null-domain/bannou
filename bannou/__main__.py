from bannou import client, bot_settings

try:
    import uvloop

    uvloop.install()
except ImportError:
    print("uvloop is not installed, falling back to asyncio")

bot = client.build_bot(bot_settings)

bot.run()
