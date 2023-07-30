"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Not
from vkbotkit.objects.filters.message import IsCommand
from assets.utils.user_is_sysadmin import UserIsSysAdmin


quit_set = ["quit", "выход"]
post_to_telegram = ["post", "пост"]
post_to_twitter = ["tweet", "твитнуть", "твит"]

BotAdminQuit = UserIsSysAdmin & IsCommand(quit_set, only_without_args=True)
NotBotAdminQuit = Not(UserIsSysAdmin) & IsCommand(quit_set, only_without_args=True)

TGBotAdminPost = UserIsSysAdmin & IsCommand(post_to_telegram, only_with_args=True)
TGNotBotAdmin = Not(UserIsSysAdmin) & IsCommand(post_to_telegram)
TGNoArgs = UserIsSysAdmin & IsCommand(post_to_telegram, only_without_args=True)

TWBotAdminPost = UserIsSysAdmin & IsCommand(post_to_twitter, only_with_args=True)
TWNotBotAdmin = Not(UserIsSysAdmin) & IsCommand(post_to_twitter)
TWNoArgs = UserIsSysAdmin & IsCommand(post_to_twitter, only_without_args=True)
