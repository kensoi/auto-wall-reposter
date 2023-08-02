"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.message import IsCommand


RulesCommand = IsCommand(["правила", "rules"])
HelpCommand = IsCommand(["помощь", "команды", "help", "commands"])
