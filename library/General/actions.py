"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library, callback
from vkbotkit.objects.filters.actions import *
from vkbotkit.objects.enums import NameCases

from .templates import CHAT_CREATE, NEW_USER


class ActionReactions(Library):
    @callback(ChatCreate)
    async def chat_create(self, toolkit, package):
        await toolkit.messages.send(package, CHAT_CREATE)

    @callback(ChatInviteUser | ChatInviteUserByLink)
    async def new_user(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.action.member_id, None, NameCases.NOM)

        response = NEW_USER.format(
            bot_mention = toolkit.bot_mentions[0],
            user_mention = user_mention
        )
        
        await toolkit.messages.send(package, response)
