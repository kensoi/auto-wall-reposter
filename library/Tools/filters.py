"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.filters.filter import Filter, Not
from utils import init


@init
class LengthLimit(Filter):
    async def check(self, _, package):
        if "items" not in package.raw:
            return
        
        return len(package.items) == 3

ShortLink=IsCommand(["сократить"])

ShortLinkArgsTrouble = ShortLink & Not(LengthLimit)
ShortLinkArgs = ShortLink & LengthLimit