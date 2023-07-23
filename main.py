"""
Copyright 2022 kensoi
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from utils.flask import keep_alive

# asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# load environment values and patching Repl.It

load_dotenv()
debug_mode = os.environ.get('DEBUG_MODE', "False") == "True" or "-d" in sys.argv
keep_alive(debug_mode)

if __name__ == "__main__":
    try:
        from utils.bot import bot
        
        miuruwa_bot = bot(debug_mode)
        loop.run_until_complete(miuruwa_bot)

    except KeyboardInterrupt:
        loop.close()