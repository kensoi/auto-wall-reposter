from os import getenv

from vkbotkit import Bot
from vkbotkit.objects import enums


async def bot(debug_mode = False):
    """
    Корень приложения VKBotKit v1.3 для работы через сообщество

    debug_mode: bool - запуск бота с debug токеном
    """

    if debug_mode:
        token = getenv('DEBUG_TOKEN')
        group_id = int(getenv('DEBUG_ID'))
        log_level = enums.LogLevel.DEBUG

    else:
        token = getenv('PUBLIC_TOKEN')
        group_id = int(getenv('PUBLIC_ID'))
        log_level = enums.LogLevel.INFO

    log_to_file = True
    log_to_console = True

    bot = Bot(token, group_id)
    bot.toolkit.configure_logger(log_level, log_to_file, log_to_console)
    bot.toolkit.bot_mentions=getenv('BOT_MENTIONS').split(" ")

    # START POLLING
    await bot.start_polling()