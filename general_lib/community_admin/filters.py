"""
copyright 2025 miuruwa
"""

from vkbotkit.objects.filters.events import WhichEvent, Events
from vkbotkit.objects.filters.message import IsUserChat
from vkbotkit.objects.filters.filter import Filter
from vkbotkit.objects.mention import Mention
from assets.utils.init import init


@init
class NotCommand(Filter):
    """
    NotCommand filter
    """

    async def check(self, toolkit, package) -> bool | None:
        """
        Check method
        """

        if package.type is not Events.MESSAGE_NEW:
            return True

        if isinstance(package.items[0], Mention):
            if toolkit.bot_is_group:
                return int(package.items[0]) != -toolkit.bot_id
            
            return int(package.items[0]) != toolkit.bot_id
            

        elif package.items[0].lower() not in toolkit.bot_mentions:
            return True

KeyboardReply = WhichEvent([Events.MESSAGE_EVENT])
NewMessageFromPrivate = IsUserChat & NotCommand
