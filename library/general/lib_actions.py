"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.actions import ChatInviteUser, ChatKickUser

from .filters import StartCommand, StartText
from .templates import REACTION_TO_NEW_USER, REACTION_TO_KICK


class ActionReactions(Library):
    @callback(StartCommand | StartText | ChatInviteUser)
    async def chat_invite_user(self, toolkit, package):
        bot_mention = await toolkit.get_my_mention()
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, REACTION_TO_NEW_USER.format(
            user_mention = repr(user_mention),
            bot_mention = repr(bot_mention)
        ))
    
    @callback(ChatKickUser)
    async def chat_kick_user(self, toolkit, package):
        await toolkit.messages.send(package, REACTION_TO_KICK)