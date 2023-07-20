"""
Copyright 2023 kensoi
"""
import asyncio

from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

from os import getenv
from sys import argv

from vkbotkit.objects import callback, Library

from vkbotkit.objects.filters.filter import Filter
from vkbotkit.objects.enums import Events, LogLevel

import tweepy

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
    TWITTER_BEARER_KEY = getenv("TWITTER_BEARER_TOKEN")
    TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")

    return tweepy.Client(
        TWITTER_BEARER_KEY, 
        TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )

def create_api():
    TWITTER_API_KEY = getenv("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
    TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_KEY_SECRET, 
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )

    return tweepy.API(auth)

async def tweet(client: tweepy.Client, toolkit, message: str, attachments=None):
    loop = asyncio.get_event_loop()
    _executor = ThreadPoolExecutor(10)

    if attachments:
        api = await loop.run_in_executor(_executor, lambda _: create_api(), None)
        session = toolkit._session
        photo_list = []
        media_ids = []

        for attachment in attachments:
            if attachment.type == "photo":
                max_height = 0
                url = ""
                
                for version in attachment.photo.sizes:
                    if version.height > max_height:
                        url = version.url
                        max_height = version.height

                async with session.get(url) as resp:
                    photo = await resp.read()
                    photo_list.append(photo) 

                if len(photo_list) == 4:
                    break
        
        for photo in photo_list:
            media_id = api.media_upload(filename=".jpg", file=BytesIO(photo))
            media_ids.append(media_id)
            
        await loop.run_in_executor(
            _executor, 
            lambda _: client.create_tweet(
                text=message,
                media_ids=media_ids
            ), None
        )

    else:
        await loop.run_in_executor(_executor, lambda _: client.create_tweet(text=message), None)

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

            await tweet(self.client, toolkit, package.text, package.attachments)
            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)