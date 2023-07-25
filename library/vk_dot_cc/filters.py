"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Filter
from vkbotkit.objects.filters.message import IsCommand

init = lambda definition: definition()

@init
class LengthLimit(Filter):
    async def check(self, _, package):
        if "items" not in package.raw:
            return
        
        return len(package.items) == 3
    
Request = IsCommand({"сократить", "сократи"}, only_with_args=True)
RequestWithoutLink = IsCommand({"сократить", "сократи"}, only_with_args=False)