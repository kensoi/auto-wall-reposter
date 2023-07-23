"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases, Events
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.filters.events import WhichEvent

# Filter helper
init = lambda definition: definition()

# Filters

RulesRequest = IsCommand({"правила", "rules"}, only_without_args=True)
CommandListRequest = IsCommand({"команды", "commands"}, only_without_args=True)
IsReaction = WhichEvent({Events.MESSAGE_REACTION_EVENT, })

# Message reaction templates

REACTION_WITH_RULES = """
{user_mention}, правила можно найти в соответствующем обсуждении: {topic_link}
"""

REACTION_WITH_COMMANDS = """
{user_mention}, список команд можно найти в соответствующем обсуждении: {topic_link}
"""

STOP_REACTION = """
Хорошо, завершаю работу.
"""

ERROR_REACTION = """
{user_mention}, вам нельзя проворачивать такую аферу.
"""

REACT_THANK = "{reactor_mention}, спасибо за реакцию!"


class Main(Library):
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

    @callback(IsReaction)
    async def thank_for_reaction(self, toolkit, package):
        reactor_mention = await toolkit.create_mention(package.reacted_id)

        await toolkit.messages.send(package, REACT_THANK.format(reactor_mention = repr(reactor_mention)))

        

        