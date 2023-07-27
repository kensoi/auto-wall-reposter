"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases

from .filters import RulesRequest, CommandListRequest
from .templates import REACTION_WITH_RULES, REACTION_WITH_COMMANDS


class GeneralReplies(Library):
    """
    General replies library
    """

    @callback(RulesRequest)
    async def send_rules(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, REACTION_WITH_RULES.format(
            user_mention = repr(user_mention),
            topic_link = os.environ.get("RULES_LINK")
        ))

    @callback(CommandListRequest)
    async def send_commands(self, toolkit, package):
        bot_mention = await toolkit.get_my_mention()
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, REACTION_WITH_COMMANDS.format(
            user_mention = repr(user_mention),
            bot_mention = repr(bot_mention),
            topic_link = os.environ.get("COMMANDS_LINK")
        ))