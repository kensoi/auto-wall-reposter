"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.message import IsCommand, IsThatText


StartCommand = IsCommand({"старт",}, only_without_args=True)
StartText = IsThatText({"Начать", "начать"})
