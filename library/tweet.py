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
from vkbotkit.objects.filters.message import IsCommand
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

_executor = ThreadPoolExecutor(10)
api = create_api()

async def upload_photo_on_twitter(attachment, session):
    loop = asyncio.get_event_loop()
    size_list = list(map(
            lambda item: {
                "url": item.url,
                "height": item.height
            },
            attachment.photo.sizes
        ))
    size_list.sort(key=lambda item: item["height"])
    
    async with session.get(size_list[-1]["url"]) as resp:
        photo = await resp.read()

    media_object = await loop.run_in_executor(
        _executor, 
        lambda _: api.media_upload(filename=".jpg", file=BytesIO(photo)), 
        None
    )
    return media_object.media_id


async def tweet(client: tweepy.Client, toolkit, message: str, attachments=None):
    loop = asyncio.get_event_loop()

    if not attachments:
        await loop.run_in_executor(_executor, lambda _: client.create_tweet(text=message), None)
        return
    
    photo_attachments = list(filter(
        lambda item: item.type == "photo", attachments
    ))

    if len(photo_attachments) == 0:
        await loop.run_in_executor(_executor, lambda _: client.create_tweet(text=message), None)
        return
    
    photo_attachments[:min(len(photo_attachments),4)]
    
    media_ids = await asyncio.gather(*[
        upload_photo_on_twitter(photo, toolkit._session) for photo in photo_attachments
    ])
    
    await loop.run_in_executor(
        _executor, 
        lambda _: client.create_tweet(
            text=message,
            media_ids=media_ids
        ), None
    )


TWEET_TEMPLATE = "Новый пост! Ссылка: {link_to_post}"

EXCEPTION_MESSAGE = "Твит не был создан. Причина: {exception}"
NO_ERRORS="Твит отправлен"
RIGHTS_ERROR="У вас нет полномочий на эту команду."

NO_MESSAGE="""
Попробуйте написать "{bot_mention} твитнуть Привет, мир!"
"""

class Main(Library):
    """
    Библиотека которая дублирует посты из группы вк как твиты в твиттере
    """
    client=None

    @callback(NewPost())
    async def repost(self, toolkit, package):
        try:
            if not self.client:
                self.client = create_client()

            await tweet(self.client, toolkit, package.text, package.attachments)
            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)


    @callback(IsCommand({"tweet", "твит", "твитнуть"}))
    async def tweet(self, toolkit, package):
        if package.from_id != int(getenv("BOT_ADMIN_ID")):
            await toolkit.messages.send(package, RIGHTS_ERROR)
            return

        if len(package.items) == 2:
            bot_mention = await toolkit.get_my_mention()

            await toolkit.messages.send(package, NO_MESSAGE.format(bot_mention = repr(bot_mention)))
            return

        try:
            print(package.attachments)

            if not self.client:
                self.client = create_client()

            await tweet(self.client, toolkit, " ".join(package.items[2:]), package.attachments)

            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)
            await toolkit.messages.send(package, NO_ERRORS)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)
            await toolkit.messages.send(package, EXCEPTION_MESSAGE.format(exception=e))
