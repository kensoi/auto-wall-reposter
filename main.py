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

from assets.utils.init import init

load_dotenv()
debug_mode = os.environ.get('DEBUG_MODE') == "True" or "-d" in sys.argv

async def start_polling():
    """
    parse for packages from server while bot.toolkit.is_polling
    """

    # Marcel Bot

    canary_token = os.environ.get('ACCESS_TOKEN_CANARY')
    canary_bot_id = int(os.environ.get('BOT_ID_CANARY'))

    canary_bot = Bot(canary_token, canary_bot_id)

    # Miuruwa Poll Bot

    miuruwa_token = os.environ.get('ACCESS_TOKEN_MIURUWA')
    miuruwa_bot_id = int(os.environ.get('BOT_ID_MIURUWA'))

    miuruwa_bot = Bot(miuruwa_token, miuruwa_bot_id)

    log_level = LogLevel.DEBUG if debug_mode else LogLevel.INFO

    @init
    async def poll_miuruwa():
        """
        Отслеживатель событий из Miuruwa ~* в ВК
        - все новые посты отсылает в беседу
        """
        miuruwa_bot.toolkit.configure_logger(log_level, True, True)

        miuruwa_plugin_manager = PluginManager(canary_bot.toolkit)
        miuruwa_plugin_manager.import_library("miuruwa")

        async for package in miuruwa_bot.poll_server():
            await miuruwa_plugin_manager.handle(package)

    @init
    async def poll_marcel():
        """
        Отслеживатель событий из Менеджера Кани в ВК
        - все новые посты отсылает в беседу
        """
        canary_bot.toolkit.bot_mentions = os.environ.get("BOT_MENTIONS", "").split(" ")
        canary_bot.toolkit.configure_logger(log_level, True, True)

        canary_plugin_manager = PluginManager(canary_bot.toolkit)
        canary_plugin_manager.import_library("marcel")

        async for package in canary_bot.poll_server():
            await canary_plugin_manager.handle(package)

    # Параллельное отслеживание событий в обоих группах.
    await asyncio.gather(poll_miuruwa, poll_marcel)

if __name__ == "__main__":
    keep_alive(debug_mode)
    asyncio.run(start_polling())
