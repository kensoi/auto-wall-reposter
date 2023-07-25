"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.filters.filter import Filter


# Filter helper
init = lambda definition: definition()

# Filters

@init
class isSysAdmin(Filter):
    async def check(self, _, package):
        if "from_id" not in package.raw:
            return
        
        return package.from_id != int(os.environ.get("BOT_ADMIN_ID"))
    
StopBotRequest = IsCommand({"выход", "stop"}, only_without_args=True)
