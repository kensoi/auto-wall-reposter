"""
Copyright 2022 kensoi
"""

import asyncio
import sys
from dotenv import load_dotenv
from bot import bot

if "vkbotkit" not in sys.modules:
    import pip
    pip.main(["install", "-r", "requirements.txt"])

from background import keep_alive

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    load_dotenv()
    keep_alive()
    loop.run_until_complete(bot())
