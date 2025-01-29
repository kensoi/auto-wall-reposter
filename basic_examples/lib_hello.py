"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import callback, Library
from vkbotkit.objects.filters.actions import ChatInviteUser
from vkbotkit.objects.filters.message import IsThatText, IsCommand


HELLO_MESSAGE = """
Hello, world
Programmed to work and not to feel
Not even sure that this is real
"""
HELP_MESSAGE = """
HELP INSTRUCTIONS HERE
"""


class Main(Library):
    """
    Библиотека с командами, предназначенными для приветствия пользователей
    """

    @callback(IsCommand({"start",}) | IsThatText({"Начать",}) | ChatInviteUser())
    async def send_hello(self, toolkit, package):
        """
        при получении команды '@your_bot_id start' => отправлять текст HELLO_ME
        """
        await toolkit.messages.send(package, HELLO_MESSAGE)


    @callback(IsCommand({"help",}) | IsThatText({"Помощь",}))
    async def send_help(self, toolkit, package):
        """
        при получении команды '@your_bot_id start' => отправлять текст HELLO_ME
        """

        await toolkit.messages.send(package, HELP_MESSAGE)
        