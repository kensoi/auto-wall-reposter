"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.enums import NameCases

from .filters import (
    BotAdminQuit,
    NotBotAdminQuit
)
from .templates import (
    USER_IS_NOT_BOT_ADMIN,
    QUIT_MESSAGE
)


class StopBot(Library):
    """
    Stop bot
    """

    @callback(NotBotAdminQuit)
    async def unknown_user(self, toolkit, package):
        """
        User has no bot-admin rights
        """

        await toolkit.messages.send(package, QUIT_MESSAGE)

    @callback(BotAdminQuit)
    async def stop_bot(self, toolkit, package):
        """
        stop poll
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        with USER_IS_NOT_BOT_ADMIN.format(user_mention=user_mention) as response:
            await toolkit.messages.send(package, response)
