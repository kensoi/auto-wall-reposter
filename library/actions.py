"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.actions import ChatInviteUser, ChatKickUser
from vkbotkit.objects.filters.message import IsCommand, IsThatText

NewUser = IsCommand({"старт",}, only_without_args=True) | IsThatText({"Начать", "начать"}) | ChatInviteUser()
KickUser = ChatKickUser()

reaction_to_new_user = """
Привет, {user_mention}! Мы рады вашему вступлению! 
Чтобы получить список команд для бота, напишите "{bot_mention} команды"
"""

reaction_to_kick = """Приносим соболезнования."""

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