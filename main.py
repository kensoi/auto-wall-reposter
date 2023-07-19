"""
Copyright 2022 kensoi
"""

import asyncio
import sys
from os import getenv
from dotenv import load_dotenv
from utils.replit_patch import replit_patch

# asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# load environment values and patching Repl.It

load_dotenv()
debug_mode = "-d" in sys.argv or getenv('DEBUG_MODE') == "True"
replit_patch(debug_mode)

if __name__ == "__main__":
    try:
        from utils.bot import bot
        
        miuruwa_bot = bot(debug_mode)
        loop.run_until_complete(miuruwa_bot)

    except KeyboardInterrupt:
        loop.close()