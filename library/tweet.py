"""
Copyright 2023 kensoi
"""

from os import getenv
from sys import argv

from vkbotkit.objects import callback, Library

from vkbotkit.objects.filters.filter import Filter
from vkbotkit.objects.enums import Events, LogLevel

import tweepy
from tweepy.errors import TweepyException

class NewPost(Filter):
    async def check(self, _, package):
        return package.type == Events.WALL_POST_NEW

def get_wall_object(wall):
        return f"wall{wall.owner_id}_{wall.id}"
    
def get_chat_id():
    if "-d" in argv or getenv('DEBUG_MODE'):
        return getenv('DEBUG_CHAT_TO_REPOST')
    
    return getenv('CHAT_TO_REPOST')

def create_client():
    TWITTER_API_KEY = getenv("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
    TWITTER_BEARER_KEY = getenv("TWITTER_BEARER_KEY")
    TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")

    return tweepy.Client(
        TWITTER_BEARER_KEY, 
        TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )

def tweet(client: tweepy.Client, message: str):
    client.create_tweet(text=message)

    print('Tweeted successfully!')

TWEET_TEMPLATE = "Новый пост! Ссылка: {link_to_post}"

EXCEPTION_MESSAGE = "Твит не был создан. Причина: {exception}"
NO_ERRORS="Твит отправлен"

class Main(Library):
    """
    Библиотека которая дублирует посты из группы вк как твиты в твиттере
    """
    client=None

    @callback(NewPost())
    async def repost(self, toolkit, package):
        wall_id = get_wall_object(package)

        try:
            if not self.client:
                self.client = create_client()

            tweet(self.client, TWEET_TEMPLATE.format(link_to_post=f"vk.com/{wall_id}"))
            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)