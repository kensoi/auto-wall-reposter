"""
Copyright 2023 kensoi
"""

from os import getenv

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.message import IsCommand


RulesRequest = IsCommand({"правила",})
CommandListRequest = IsCommand({"команды", "помощь",})
StopBotRequest = IsCommand({"выход",})

reaction_with_rules = """
{user_mention}, правила можно найти в соответствующем обсуждении: {topic_link}
"""

reaction_with_commands = """
{user_mention}, вот ваш список команд:

{bot_mention} команды - получить список команд для чат-бота.
{bot_mention} правила - получить список правил беседы "Миурува на каждый день"
"""

reaction_to_attempt_to_stop = """
Хорошо, завершаю работу.
"""

reaction_to_attempt_to_stop_with_no_rights = """
{user_mention}, вам нельзя проворачивать такую аферу.
"""

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

        

        