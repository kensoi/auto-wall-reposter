"""
copyright 2025 miuruwa
"""

import os

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases

from .templates import RULES_VECTOR, COMMANDS_VECTOR
from .filters import RulesCommand, HelpCommand


class UsefulLinks(Library):
    """
    Reactions that send links to rules and commands
    """

    @callback(RulesCommand)
    async def rules(self, toolkit, package):
        """
        Rules topic
        """

        link = os.environ.get("RULES_LINK")
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        response = RULES_VECTOR.format(user_mention = user_mention, link = link)

        await toolkit.messages.send(package, response)

    @callback(HelpCommand)
    async def help(self, toolkit, package):
        """
        Command topic
        """

        link = os.environ.get("COMMAND_GUIDE_LINK")
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        response = COMMANDS_VECTOR.format(user_mention = user_mention, link = link)
        
        await toolkit.messages.send(package, response)
