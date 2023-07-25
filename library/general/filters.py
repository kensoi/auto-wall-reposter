"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.message import IsCommand


# Filter helper
init = lambda definition: definition()

# Filters

RulesRequest = IsCommand({"правила", "rules"}, only_without_args=True)
CommandListRequest = IsCommand({"команды", "commands"}, only_without_args=True)
