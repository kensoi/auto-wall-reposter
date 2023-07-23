"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import callback, Library
from vkbotkit.utils import gen_random

from vkbotkit.objects.filters.events import WhichEvent
from vkbotkit.objects.enums import Events


NewPost = WhichEvent(Events.WALL_POST_NEW)

class Main(Library):
    """
    Repost a post to specified group
    """

    @callback(NewPost)
    async def repost(self, toolkit, package):
        chat_id = os.environ.get('CHAT_TO_REPOST')
        wall_id = "wall{owner_id}_{post_id}".format(
            owner_id = package.owner_id,
            post_id = package.id
        )
        
        await toolkit.api.messages.send(
            random_id = gen_random(),
            peer_id = chat_id,
            attachment = wall_id,
        )
