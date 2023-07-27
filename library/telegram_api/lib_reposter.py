"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback

from .api import post_message
from .filters import NewPost
from .templates import MESSAGE_TEMPLATE


class Reposter(Library):
    """
    Repost a post to specified telegram channel
    """

    @callback(NewPost)
    async def repost(self, _, package):
        post_link = "https://vk.com/wall{owner_id}_{post_id}".format(
            owner_id = package.owner_id,
            post_id = package.id
        )

        await post_message(MESSAGE_TEMPLATE.format(link=post_link))
        

