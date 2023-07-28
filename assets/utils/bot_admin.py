"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects.filters.filter import Filter

from .init import init


@init
class isBotAdmin(Filter):
    async def check(self, _, package):
        if "from_id" not in package.raw:
            return
        
        return package.from_id == int(os.environ.get("BOT_ADMIN_ID"))
