"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Negation
from vkbotkit.objects.filters.message import IsCommand, IsUserAdmin, IsUserChat, IsBotAdmin


RequestFromChat = IsCommand({"кик", "исключить", "выкинуть"}) & IsUserChat()
NoBotAdminRules = IsCommand({"кик", "исключить", "выкинуть"}) & Negation(IsBotAdmin())
RequestFromUser = IsCommand({"кик", "исключить", "выкинуть"}) & IsBotAdmin() & Negation(IsUserAdmin())
RequestWithAdminRights = IsCommand({"кик", "исключить", "выкинуть"}) & IsBotAdmin() & IsUserAdmin()
