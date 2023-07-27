"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases

from .templates import RULES_VECTOR, COMMANDS_VECTOR
from .filters import RulesCommand, HelpCommand


class UsefulLinks(Library):
    @callback(RulesCommand)
    async def rules(self, toolkit, package):
        link = os.environ.get("RULES_LINK")
        user_mention = await toolkit.create_mention(package.action.member_id, None, NameCases.NOM)

        response = RULES_VECTOR.format(
            user_mention = user_mention,
            link = link
        )
        
        await toolkit.messages.send(package, response)

    @callback(HelpCommand)
    async def help(self, toolkit, package):
        link = os.environ.get("COMMANDS_LINK")
        user_mention = await toolkit.create_mention(package.action.member_id, None, NameCases.NOM)
        
        response = COMMANDS_VECTOR.format(
            user_mention = user_mention,
            link = link
        )

        await toolkit.messages.send(package, response)