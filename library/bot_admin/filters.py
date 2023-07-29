"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Not
from vkbotkit.objects.filters.message import IsCommand
from assets.utils.bot_admin import isBotAdmin


quit_set = ["quit", "выход"]
post_to_telegram = ["post", "пост"]
post_to_twitter = ["tweet", "твитнуть", "твит"]

BotAdminQuit = isBotAdmin & IsCommand(quit_set, only_without_args=True)
NotBotAdminQuit = Not(isBotAdmin) & IsCommand(quit_set, only_without_args=True)

TGBotAdminPost = isBotAdmin & IsCommand(post_to_telegram, only_with_args=True)
TGNotBotAdmin = Not(isBotAdmin) & IsCommand(post_to_telegram)
TGNoArgs = isBotAdmin & IsCommand(post_to_telegram, only_without_args=True)

TWBotAdminPost = isBotAdmin & IsCommand(post_to_twitter, only_with_args=True)
TWNotBotAdmin = Not(isBotAdmin) & IsCommand(post_to_twitter)
TWNoArgs = isBotAdmin & IsCommand(post_to_twitter, only_without_args=True)
