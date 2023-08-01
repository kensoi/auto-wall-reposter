"""
Copyright 2023 kensoi
"""

import os

from .init import init


@init
class SysAdminTools:
    """
    pass
    """
    admin_list: list
    list: list
    log_chat: int
    repost_chat: int
    is_x_enabled: bool = False
    is_telegram_enabled: bool = False

    def __init__(self):
        self.admin_list = list(map(int, os.environ.get("BOT_ADMIN_ID").split(" ")))
        self.list = self.admin_list
        self.is_x_enabled = os.environ.get("IS_TWITTER_ENABLED", "True") == "True"
        self.is_telegram_enabled = os.environ.get("IS_TELEGRAM_ENABLED", "True") == "True"
        self.log_chat = int(os.environ.get("CHAT_TO_LOG", self.list[0]))
        self.repost_chat = int(os.environ.get("CHAT_TO_REPOST", self.list[0]))
