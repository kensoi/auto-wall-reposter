from os import getenv

from vkbotkit import Bot
from vkbotkit.objects import enums


async def bot(debug_mode = False):
    """
    Корень приложения VKBotKit v1.2a4 для работы через сообщество
    """

    if debug_mode:
        token = getenv('DEBUG_TOKEN')
        group_id = int(getenv('DEBUG_ID'))
        log_level = enums.LogLevel.DEBUG

    else:
        token = getenv('PUBLIC_TOKEN')
        group_id = int(getenv('PUBLIC_ID'))
        log_level = enums.LogLevel.INFO

    config_log = list(getenv("CONFIG_LOG", default = ""))
    log_to_file = "f" in config_log # вывод лога в специальный файл
    log_to_console = "c" in config_log # вывод лога в консоль

    bot = Bot(token, group_id)
    bot.toolkit.configure_logger(log_level, log_to_file, log_to_console)

    # START POLLING
    await bot.start_polling()