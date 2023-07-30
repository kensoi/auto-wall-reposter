"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Filter

from .sys_admin_tools import SysAdminTools
from .init import init


@init
class UserIsSysAdmin(Filter):
    """
    check if is it bot admin
    """

    async def check(self, _, package):
        """
        Check method
        """

        return "from_id" in package.raw and \
            package.from_id in SysAdminTools.list
