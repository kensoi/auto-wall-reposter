"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects.filters.filter import Filter, Not
from vkbotkit.objects.filters.events import WhichEvent
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.enums import Events

from utils import init


@init
class isSysAdmin(Filter):
    async def check(self, _, package):
        if "from_id" not in package.raw:
            return
        
        return package.from_id != int(os.environ.get("BOT_ADMIN_ID"))
    
PostToTweet = WhichEvent({Events.WALL_POST_NEW ,})
MessageToTweet = isSysAdmin & IsCommand({"tweet", "твит", "твитнуть"}, only_with_args=True)
TweetTrouble = isSysAdmin & IsCommand({"tweet", "твит", "твитнуть"}, only_with_args=False)
NotAdmin = Not(isSysAdmin) & IsCommand({"tweet", "твит", "твитнуть"})
