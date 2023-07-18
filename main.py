"""
Copyright 2022 kensoi
"""

import asyncio

from dotenv import load_dotenv
from bot import bot

from background import keep_alive

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    load_dotenv()
    keep_alive()
    loop.run_until_complete(bot())
