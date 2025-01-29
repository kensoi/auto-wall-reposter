"""
copyright 2025 miuruwa
"""

from vkbotkit.framework.toolkit import ToolKit
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

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        response = USER_IS_NOT_BOT_ADMIN.format(user_mention=user_mention)

        await toolkit.messages.send(package, response)

    @callback(BotAdminQuit)
    async def stop_bot(self, toolkit:ToolKit, package):
        """
        stop poll
        """

        await toolkit.messages.send(package, QUIT_MESSAGE)
        toolkit.stop_polling()
