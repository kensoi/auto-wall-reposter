"""
Copyright 2022 kensoi
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from utils.flask import keep_alive

from vkbotkit import Bot, PluginManager
from vkbotkit.objects.enums import LogLevel


load_dotenv()
debug_mode = os.environ.get('DEBUG_MODE') == "True" or "-d" in sys.argv

async def start_polling():
    """
    parse for packages from server while bot.toolkit.is_polling
    """

    token = os.environ.get('ACCESS_TOKEN')
    bot_id = int(os.environ.get('BOT_ID'))

    bot = Bot(token, bot_id)
    log_level = LogLevel.DEBUG if debug_mode else LogLevel.INFO
    bot.toolkit.configure_logger(log_level, True, True)
    bot.toolkit.bot_mentions = os.environ.get("BOT_MENTIONS", "").split(" ")

    plugin_manager = PluginManager(bot.toolkit)
    plugin_manager.import_library("library")

    async for package in bot.poll_server():
        await plugin_manager.handle(package)

if __name__ == "__main__":
    keep_alive(debug_mode)
    asyncio.run(start_polling())
