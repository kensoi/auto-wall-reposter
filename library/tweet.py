"""
Copyright 2023 kensoi
"""
import asyncio
import os
import tweepy

from concurrent.futures import ThreadPoolExecutor
from io import BytesIO


from vkbotkit.objects import callback, Library

from vkbotkit.objects.filters.filter import Filter, Negation
from vkbotkit.objects.filters.events import WhichEvent
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.enums import Events, LogLevel


init = lambda definition: definition()

_executor = ThreadPoolExecutor(10)

# Twitter API

@init
def client():
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
    TWITTER_BEARER_KEY = os.environ.get("TWITTER_BEARER_TOKEN")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    return tweepy.Client(
        TWITTER_BEARER_KEY, 
        TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )


@init
def api():
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_KEY_SECRET, 
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )

    return tweepy.API(auth)


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


async def tweet(toolkit, message: str, attachments=None):
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


# helpful filter

@init
class isSysAdmin(Filter):
    async def check(self, _, package):
        return package.from_id != int(os.environ.get("BOT_ADMIN_ID"))


# Event types

PostToTweet = WhichEvent(Events.WALL_POST_NEW)
MessageToTweet = isSysAdmin & IsCommand({"tweet", "твит", "твитнуть"}, only_with_args=True)
TweetTrouble = isSysAdmin & IsCommand({"tweet", "твит", "твитнуть"}, only_with_args=False)
NotAdmin = Negation(isSysAdmin) & IsCommand({"tweet", "твит", "твитнуть"})


# message templates

TWEET_TEMPLATE = "Новый пост! Ссылка: {link_to_post}"

EXCEPTION_MESSAGE = "Твит не был создан. Причина: {exception}"
NO_ERRORS="Твит отправлен"
RIGHTS_ERROR="У вас нет полномочий на эту команду."

NO_MESSAGE="""
Попробуйте написать "{bot_mention} твитнуть Привет, мир!"
"""


class Main(Library):
    """
    Twitter API library for VKBotKit
    """

    client=None

    @callback(PostToTweet)
    async def repost(self, toolkit, package):
        """
        Tweet with post data (message & photos)
        """
        
        try:
            await tweet(toolkit, package.text, package.attachments)
            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)


    @callback(NotAdmin)
    async def taboo(self, toolkit, package):
        await toolkit.messages.send(package, RIGHTS_ERROR)


    @callback(TweetTrouble)
    async def tweet_help(self, toolkit, package):
        """
        Send help message to user
        """
        
        bot_mention = await toolkit.get_my_mention()

        await toolkit.messages.send(package, NO_MESSAGE.format(bot_mention = repr(bot_mention)))
    

    @callback(MessageToTweet)
    async def tweet(self, toolkit, package):
        try:
            message_to_tweet = " ".join(package.items[2:])
            await tweet(toolkit, message_to_tweet, package.attachments)

            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)
            await toolkit.messages.send(package, NO_ERRORS)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)
            await toolkit.messages.send(package, EXCEPTION_MESSAGE.format(exception=e))
