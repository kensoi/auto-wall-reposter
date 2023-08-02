"""
Copyright 2023 kensoi
"""

from vkbotkit import Bot, PluginManager
from vkbotkit.objects.enums import LogLevel

def create_bot(access_token, bot_id, debug_mode, mentions=None):
    """
    Создать чат-бота
    """
    log_level = LogLevel.DEBUG if debug_mode else LogLevel.INFO

    bot = Bot(access_token, bot_id)

    if mentions:
        bot.toolkit.bot_mentions = mentions

    bot.toolkit.configure_logger(log_level, True, True)

    return bot

async def parse_poll(package_bot, parser_bot, library_name):
    """
    parse
    """

    plugin_manager = PluginManager(parser_bot.toolkit)
    plugin_manager.import_library(library_name)

    async for package in package_bot.poll_server():
        await plugin_manager.handle(package)
