"""
Copyright 2023 kensoi
"""
from os import getenv
from sys import argv

from vkbotkit.objects import callback, Library
from vkbotkit.objects.filters.filter import Filter
from vkbotkit.objects.enums import Events
from vkbotkit.utils import gen_random


class RepostWall:
    class condition(Filter):
        async def check(self, _, package):
            return package.type == Events.WALL_POST_NEW

    def convert_wall(wall):
        return f"wall{wall.owner_id}_{wall.id}"
    
    def get_chat_id():
        if "-d" in argv or getenv('DEBUG_MODE'):
            return getenv('DEBUG_CHAT_TO_REPOST')
        
        return getenv('CHAT_TO_REPOST')


class Main(Library):
    """
    Библиотека с командами, предназначенными для приветствия пользователей
    """

    @callback(RepostWall.condition())
    async def send_hello(self, toolkit, package):
        chat_id = RepostWall.get_chat_id()
        wall_id = RepostWall.convert_wall(package)
        
        await toolkit.api.messages.send(
            random_id = gen_random(),
            peer_id = chat_id,
            attachment = wall_id,
        )
