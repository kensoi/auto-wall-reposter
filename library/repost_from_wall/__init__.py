"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import callback, Library
from vkbotkit.utils import gen_random

from .utils import (
    NewPost, 
    get_chat_id,
    get_wall_object
)

class Main(Library):
    """
    Библиотека с командами, предназначенными для приветствия пользователей
    """

    @callback(NewPost())
    async def repost(self, toolkit, package):
        chat_id = get_chat_id()
        wall_id = get_wall_object(package)
        
        await toolkit.api.messages.send(
            random_id = gen_random(),
            peer_id = chat_id,
            attachment = wall_id,
        )
