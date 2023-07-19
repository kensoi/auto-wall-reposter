"""
Copyright 2023 kensoi
"""

from os import getenv
from sys import argv

from vkbotkit.objects.filters.filter import Filter
from vkbotkit.objects.enums import Events

class NewPost(Filter):
    async def check(self, _, package):
        return package.type == Events.WALL_POST_NEW

def get_wall_object(wall):
        return f"wall{wall.owner_id}_{wall.id}"
    
def get_chat_id():
    if "-d" in argv or getenv('DEBUG_MODE'):
        return getenv('DEBUG_CHAT_TO_REPOST')
    
    return getenv('CHAT_TO_REPOST')