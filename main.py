"""
Copyright 2022 kensoi
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from utils.flask import keep_alive
from utils.bot import create_bot, parse_poll


load_dotenv()
debug_mode = os.environ.get('DEBUG_MODE') == "True" or "-d" in sys.argv

async def create_marcel_bot():
    """
    marcel bot
    """

    marcel_access_token = os.environ.get('VK_MARCEL_ACCESS_TOKEN')
    marcel_bot_id = int(os.environ.get('MARCEL_BOT_ID'))
    marcel_mentions = os.environ.get("BOT_MENTIONS", "").split(" ")

    return create_bot(marcel_access_token, marcel_bot_id, debug_mode, marcel_mentions)

async def create_miuruwa_bot():
    """
    miuruwa bot
    """

    miuruwa_access_token = os.environ.get('VK_WALL_ACCESS_TOKEN')
    miuruwa_bot_id = int(os.environ.get('WALL_COMMUNITY_ID'))

    return create_bot(miuruwa_access_token, miuruwa_bot_id, debug_mode)

async def start_polling():
    """
    parse for packages from server while bot.toolkit.is_polling
    """
    marcel_bot = await create_marcel_bot()
    miuruwa_bot = await create_miuruwa_bot()

    poll_marcel = parse_poll(marcel_bot, marcel_bot, "marcel")
    poll_miuruwa = parse_poll(miuruwa_bot, marcel_bot, "miuruwa")

    # Параллельное отслеживание событий в обоих группах.

    await asyncio.gather(poll_miuruwa, poll_marcel)

if __name__ == "__main__":
    keep_alive(debug_mode)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_polling())
