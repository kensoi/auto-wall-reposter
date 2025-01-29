"""
copyright 2025 miuruwa
"""

from vkbotkit.objects.filters.filter import Filter

from .init import init


@init
class UserIsSysAdmin(Filter):
    """
    check if is it bot admin
    """

    admin_list = None

    async def check(self, toolkit, package):
        """
        Check method
        """

        if "from_id" not in package.raw:
            return

        if not self.admin_list:
            if not toolkit.bot_is_group:
                return

            self.admin_list = list(map(
                lambda item: item.id,
                await toolkit.get_bot_admins()
            ))


        return package.from_id in self.admin_list
