"""
Copyright 2023 kensoi
"""

import os

from vkbotkit import Bot
from vkbotkit.objects.enums import LogLevel


switch_logger_level = {
    False: LogLevel.INFO,
    True: LogLevel.DEBUG
}


async def start_bot(debug_mode = False):
    """
    Init bot and start polling with VKBotKit

    debug_mode: bool - enable debug messages
    """

    # Init bot

    token = os.environ.get('ACCESS_TOKEN', '')
    bot_id = os.environ.get('BOT_ID', '0')

    bot = Bot(token, int(bot_id))

    # Configure logger

    log_to_file = True
    log_to_console = True
    log_level = switch_logger_level[debug_mode]

    bot.toolkit.configure_logger(log_level, log_to_file, log_to_console)

    # Configure mentions

    bot_mentions_separator = os.environ.get("BOT_MENTIONS_SEPARATOR", " ")
    bot_mentions = os.environ.get("BOT_MENTIONS", "")
    bot.toolkit.bot_mentions = bot_mentions.split(bot_mentions_separator)

    # START POLLING

    await bot.start_polling()
