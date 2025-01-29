"""
copyright 2025 miuruwa
"""

from vkbotkit.objects.filters.filter import Not
from vkbotkit.objects.filters.message import IsCommand
from assets.utils.user_is_sysadmin import UserIsSysAdmin


quit_set = ["quit", "выход"]
post_to_telegram = ["post_tg", "пост_тг", "запостить_тг"]
post_to_twitter = ["post_x", "пост_х", "запостить_х"]

BotAdminQuit = UserIsSysAdmin & IsCommand(quit_set)
NotBotAdminQuit = Not(UserIsSysAdmin) & IsCommand(quit_set)

TGBotAdminPost = UserIsSysAdmin & IsCommand(post_to_telegram, only_with_args=True)
TGNotBotAdmin = Not(UserIsSysAdmin) & IsCommand(post_to_telegram)
TGNoArgs = UserIsSysAdmin & IsCommand(post_to_telegram, only_without_args=True)

XBotAdminPost = UserIsSysAdmin & IsCommand(post_to_twitter, only_with_args=True)
XNotBotAdmin = Not(UserIsSysAdmin) & IsCommand(post_to_twitter)
XNoArgs = UserIsSysAdmin & IsCommand(post_to_twitter, only_without_args=True)
