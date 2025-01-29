"""
copyright 2025 miuruwa
"""

from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.filters.filter import Filter, Not

from assets.utils.init import init


@init
class LengthLimit(Filter):
    """
    check for package's items' count
    """

    async def check(self, _, package):
        """
        Check method
        """

        return "items" in package.raw and len(package.items) == 3

ShortLink=IsCommand(["сократить", "сократи", "short"])

ShortLinkArgsTrouble = ShortLink & Not(LengthLimit)
ShortLinkArgs = ShortLink & LengthLimit
