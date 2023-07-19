"""
Copyright 2023 kensoi
"""

from os import getenv

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases

from library.general.utils import (
    RulesRequest, CommandListRequest, StopBotRequest, 
    reaction_with_rules,
    reaction_with_commands, 
    reaction_to_attempt_to_stop, 
    reaction_to_attempt_to_stop_with_no_rights
)

class Main(Library):
    """
    Библиотека с командами, предназначенными для приветствия пользователей
    """

    @callback(RulesRequest)
    async def send_rules(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, reaction_with_rules.format(
            user_mention = repr(user_mention),
            topic_link = getenv("RULES_LINK")
        ))
        

    @callback(CommandListRequest)
    async def send_commands(self, toolkit, package):
        bot_mention = await toolkit.get_my_mention()
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, reaction_with_commands.format(
            user_mention = repr(user_mention),
            bot_mention = repr(bot_mention)
        ))
        
    @callback(StopBotRequest)
    async def end_bot(self, toolkit, package):
        if package.from_id == int(getenv("BOT_ADMIN_ID")):
            await toolkit.messages.send(package, reaction_to_attempt_to_stop)
            quit()

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, reaction_to_attempt_to_stop_with_no_rights.format(
            user_mention = repr(user_mention),
        ))

        

        