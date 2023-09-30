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
    log_hub: int
    beta_hub: int
    repost_hub: int
    is_x_enabled: bool = False
    is_telegram_enabled: bool = False

    def __init__(self):
        self.list = []
        self.is_x_enabled = os.environ.get("IS_X_ENABLED", "True") == "True"
        self.is_telegram_enabled = os.environ.get("IS_TELEGRAM_ENABLED", "True") == "True"
        self.log_hub = int(os.environ.get("LOG_HUB"))
        self.repost_hub = int(os.environ.get("REPOST_HUB"))
        self.beta_hub = int(os.environ.get("BETA_HUB"))
