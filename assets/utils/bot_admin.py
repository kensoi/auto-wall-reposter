"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects.filters.filter import Filter

from .init import init


@init
class isBotAdmin(Filter):
    """
    check if is it bot admin
    """

    async def check(self, _, package):
        """
        Check method
        """

        return "from_id" in package.raw and package.from_id == int(os.environ.get("BOT_ADMIN_ID"))
