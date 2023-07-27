"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.message import IsCommand, IsThatText

KickMembers = IsCommand({"кик", "исключить", "выкинуть"})
RulesRequest = IsCommand({"правила", "rules"}, only_without_args=True)
StartCommand = IsCommand({"старт",}, only_without_args=True)
StartText = IsThatText({"Начать", "начать"})
CommandListRequest = IsCommand({"команды", "commands"}, only_without_args=True)
