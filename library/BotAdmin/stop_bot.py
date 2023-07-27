"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback

from .filters import (
    BotAdminQuit,
    NotBotAdminQuit
)
from .templates import (
    USER_IS_NOT_BOT_ADMIN,
    QUIT_MESSAGE
)


class StopBot(Library):
    @callback(NotBotAdminQuit)
    async def unknown_user(self, toolkit, package):
        await toolkit.messages.send(package, QUIT_MESSAGE)

    @callback(BotAdminQuit)
    async def unknown_user(self, toolkit, package):
        await toolkit.messages.send(package, USER_IS_NOT_BOT_ADMIN)