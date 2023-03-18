from __future__ import annotations

from bannou import client

try:
    import uvloop

    uvloop.install()
except ImportError:
    print("uvloop is not installed, falling back to asyncio")

bot = client.build_bot()
bot.run()
