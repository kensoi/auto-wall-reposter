"""
Copyright 2023 kensoi
"""

import asyncio
import os

from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import aiohttp
import tweepy

from assets.utils.init import init

_executor = ThreadPoolExecutor(10)
session = aiohttp.ClientSession()

async def run_in_executor(func):
    """
    run function by asynchronous way
    """

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, func, None)

@init
def client():
    """
    X client
    """

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
    """
    X API
    """

    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )

    return tweepy.API(auth)

async def upload_photo_on_twitter(attachment):
    """
    upload photo on X
    """

    photo = max(attachment.photo.sizes, key=lambda photo: photo.height)

    async with session.get(photo.url) as resp:
        photo = await resp.read()

    media_object = await run_in_executor(
        lambda _: api.media_upload(filename=".jpg", file=BytesIO(photo))
    )

    return media_object.media_id

async def tweet(_, message: str, attachments=None):
    """
    tweet post on X
    """

    if not attachments:
        return await run_in_executor(lambda _: client.create_tweet(text=message))

    photo_attachments = list(filter(
        lambda item: item.type == "photo", attachments
    ))

    if len(photo_attachments) == 0:
        return await run_in_executor(lambda _: client.create_tweet(text=message))

    photo_attachments = photo_attachments[:min(len(photo_attachments),4)]

    media_ids = await asyncio.gather(*[
        upload_photo_on_twitter(photo) for photo in photo_attachments
    ])

    await run_in_executor(
        lambda _: client.create_tweet(
            text=message,
            media_ids=media_ids
        )
    )
