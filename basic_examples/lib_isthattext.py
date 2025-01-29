"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import callback, Library
from vkbotkit.objects.filters.message import IsThatText


class Main(Library):
    """
    Библиотека с командами, предназначенными для приветствия пользователей
    """

    @callback(IsThatText({"привет",}))
    async def send_hello(self, toolkit, package):
        """
        при получении "привет" отвечает приветствием
        """
        await toolkit.messages.send(package, "приветик")


    @callback(IsThatText({"пока",}))
    async def send_goodbye(self, toolkit, package):
        """
        при получении "пока" отвечает прощанием
        """
        await toolkit.messages.send(package, "и тебе пока")
