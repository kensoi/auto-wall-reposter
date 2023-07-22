"""
Copyright 2023 kensoi
"""

from os import getenv

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases, Events
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.filters.events import WhichEvent

RulesRequest = IsCommand({"правила", "rules"}, only_without_args=True)
CommandListRequest = IsCommand({"команды", "commands"}, only_without_args=True)
StopBotRequest = IsCommand({"выход", "stop"}, only_without_args=True)
IsReaction = WhichEvent({Events.MESSAGE_REACTION_EVENT, })

reaction_with_rules = """
{user_mention}, правила можно найти в соответствующем обсуждении: {topic_link}
"""

reaction_with_commands = """
{user_mention}, список команд можно найти в соответствующем обсуждении: {topic_link}
"""

reaction_to_attempt_to_stop = """
Хорошо, завершаю работу.
"""

reaction_to_attempt_to_stop_with_no_rights = """
{user_mention}, вам нельзя проворачивать такую аферу.
"""

react_thank = "{reactor_mention}, спасибо за реакцию!"

class Main(Library):
    """
    Библиотека с базовыми командами
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
            bot_mention = repr(bot_mention),
            topic_link = getenv("COMMANDS_LINK")
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

    @callback(IsReaction)
    async def thank_for_reaction(self, toolkit, package):
        reactor_mention = await toolkit.create_mention(package.reacted_id)

        await toolkit.messages.send(package, react_thank.format(reactor_mention = repr(reactor_mention)))

        

        