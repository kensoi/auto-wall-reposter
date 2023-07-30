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
    list: list

    def __init__(self):
        bot_admin_id = os.environ.get("BOT_ADMIN_ID")
        self.list = list(map(int, bot_admin_id.split(" ")))
