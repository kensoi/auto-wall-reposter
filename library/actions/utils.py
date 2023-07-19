"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.actions import ChatInviteUser, ChatKickUser
from vkbotkit.objects.filters.message import IsCommand, IsThatText

NewUser = IsCommand({"старт",}) | IsThatText({"Начать", "начать"}) | ChatInviteUser()
KickUser = ChatKickUser()

reaction_to_new_user = """
Привет, {user_mention}! Мы рады вашему вступлению! 
Чтобы получить список команд для бота, напишите "{bot_mention} команды"
"""

reaction_to_kick = """Приносим соболезнования."""