"""
Copyright 2022 kensoi
"""

import asyncio
import sys
from os import getenv
from dotenv import load_dotenv
load_dotenv()


debug_mode = "-d" in sys.argv or getenv('DEBUG_MODE') == "True"

if not debug_mode:
    if "vkbotkit" not in sys.modules:
        import pip
        pip.main(["install", "-r", "requirements.txt"])
        
    keep_alive()

from utils.background import keep_alive
from bot import bot

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

if __name__ == "__main__":

    loop.run_until_complete(bot(debug_mode))
