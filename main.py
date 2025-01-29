"""
copyright 2025 miuruwa
"""

import asyncio
import os
import sys
from dotenv import load_dotenv


load_dotenv()
debug_mode = os.environ.get('DEBUG_MODE') == "True" or "-d" in sys.argv

from utils.flask import keep_alive
from utils.bot import create_bot, parse_poll


async def create_marcel_bot():
    """
    marcel bot
    """

    marcel_access_token = os.environ.get('VK_MARCEL_ACCESS_TOKEN')
    marcel_bot_id = int(os.environ.get('MARCEL_BOT_ID')) # type: ignore
    marcel_mentions = os.environ.get("BOT_MENTIONS", "").split(" ")

    return create_bot(marcel_access_token, marcel_bot_id, debug_mode, marcel_mentions)


async def create_repost_bot():
    """
    social media repost module
    """

    repost_access_token = os.environ.get('VK_WALL_ACCESS_TOKEN')
    repost_bot_id = int(os.environ.get('WALL_COMMUNITY_ID')) # type: ignore

    return create_bot(repost_access_token, repost_bot_id, debug_mode)


async def start_polling():
    """
    parse for packages from server while bot.toolkit.is_polling
    """
    poll_tasks = []
    general_bot = await create_marcel_bot()
    reposter_bot = await create_repost_bot()

    poll_general = parse_poll(reposter_bot, reposter_bot, "general_lib", debug_mode)
    poll_tasks.append(poll_general)

    if not debug_mode:
        poll_reposter = parse_poll(general_bot, reposter_bot, "content_repost", False)
        poll_tasks.append(poll_reposter)

    # Параллельное отслеживание событий в обоих группах.

    await asyncio.gather(*poll_tasks)

if __name__ == "__main__":
    keep_alive(debug_mode)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_polling())
