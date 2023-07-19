"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases

from library.actions.utils import (
    NewUser, KickUser,
    reaction_to_new_user, reaction_to_kick
)

class Main(Library):
    @callback(NewUser)
    async def chat_invite_user(self, toolkit, package):
        bot_mention = await toolkit.get_my_mention()
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, reaction_to_new_user.format(
            user_mention = repr(user_mention),
            bot_mention = repr(bot_mention)
        ))
    
    @callback(KickUser)
    async def chat_kick_user(self, toolkit, package):
        await toolkit.messages.send(package, reaction_to_kick)