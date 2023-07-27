"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects.filters import Filter, Not
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.filters.events import WhichEvent, Events

from utils import init

NewPost = WhichEvent({Events.WALL_POST_NEW, })

@init
class isSysAdmin(Filter):
    async def check(self, _, package):
        if "from_id" not in package.raw:
            return
        
        return package.from_id != int(os.environ.get("BOT_ADMIN_ID"))
    
MessageToPost = isSysAdmin & IsCommand({"пост", "post"}, only_with_args=True)
PostTrouble = isSysAdmin & IsCommand({"пост", "post"}, only_with_args=False)
NotAdmin = Not(isSysAdmin) & IsCommand({"пост", "post"})