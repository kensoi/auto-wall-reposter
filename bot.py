"""
Copyright 2022 kensoi
"""

import asyncio
from os import getenv
from sys import argv

from dotenv import load_dotenv
from vkbotkit import Bot
from vkbotkit.objects import enums


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def main():
    """
    Корень приложения VKBotKit v1.2a4 для работы через сообщество
    """

    if "-d" in argv or getenv('DEBUG_MODE'):
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


if __name__ == "__main__":
    load_dotenv()
    loop.run_until_complete(main())
