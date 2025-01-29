"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.actions import (
    ChatCreate,
    ChatInviteUser,
    ChatInviteUserByLink
)

from .templates import CHAT_CREATE, NEW_USER


class ActionReactions(Library):
    """
    Reactions to actions
    """

    @callback(ChatCreate)
    async def chat_create(self, toolkit, package):
        """
        Chat is created
        """

        await toolkit.messages.send(package, CHAT_CREATE)

    @callback(ChatInviteUser | ChatInviteUserByLink)
    async def new_user(self, toolkit, package):
        """
        New user at chat
        """

        bot_mention = toolkit.bot_mentions[0]
        user_mention = await toolkit.create_mention(package.action.member_id, None, NameCases.NOM)
        response = NEW_USER.format(bot_mention = bot_mention, user_mention = user_mention)

        await toolkit.messages.send(package, response)
