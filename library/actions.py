"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.actions import ChatInviteUser, ChatKickUser
from vkbotkit.objects.filters.message import IsCommand, IsThatText

StartCommand = IsCommand({"старт",}, only_without_args=True)
StartText = IsThatText({"Начать", "начать"})

REACTION_TO_NEW_USER = """
Привет, {user_mention}! Мы рады вашему вступлению! 
Чтобы получить список команд для бота, напишите "{bot_mention} команды"
"""

REACTION_TO_KICK = """Приносим соболезнования."""

class Main(Library):
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