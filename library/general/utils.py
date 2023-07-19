"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.message import IsThatText, IsCommand


RulesRequest = IsCommand({"правила",})
CommandListRequest = IsCommand({"команды", "помощь",}) | IsThatText({"Помощь", "помощь"})
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