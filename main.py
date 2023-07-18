"""
Copyright 2022 kensoi
"""

import asyncio
import sys
from os import getenv
from dotenv import load_dotenv

if "vkbotkit" not in sys.modules:
    import pip
    pip.main(["install", "-r", "requirements.txt"])

from background import keep_alive
from bot import bot

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    load_dotenv()

    debug_mode = "-d" in sys.argv or getenv('DEBUG_MODE') == "True"

    if not debug_mode:
        keep_alive()

    loop.run_until_complete(bot(debug_mode))
