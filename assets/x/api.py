"""
copyright 2025 miuruwa
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

    X_API_KEY = os.environ.get("X_API_KEY")
    X_API_KEY_SECRET = os.environ.get("X_API_KEY_SECRET")
    X_BEARER_KEY = os.environ.get("X_BEARER_TOKEN")
    X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
    X_SECRET_TOKEN = os.environ.get("X_SECRET_TOKEN")

    return tweepy.Client(
        X_BEARER_KEY,
        X_API_KEY, X_API_KEY_SECRET,
        X_ACCESS_TOKEN, X_SECRET_TOKEN
    )

@init
def api():
    """
    X API
    """

    X_API_KEY = os.environ.get("X_API_KEY")
    X_API_KEY_SECRET = os.environ.get("X_API_KEY_SECRET")
    X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
    X_SECRET_TOKEN = os.environ.get("X_SECRET_TOKEN")

    auth = tweepy.OAuth1UserHandler(
        X_API_KEY, X_API_KEY_SECRET,
        X_ACCESS_TOKEN, X_SECRET_TOKEN
    )

    return tweepy.API(auth)

async def upload_photo(attachment):
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

async def post_on_x(message: str, attachments=None):
    """
    create post on X
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
        upload_photo(photo) for photo in photo_attachments
    ])

    await run_in_executor(
        lambda _: client.create_tweet(
            text=message,
            media_ids=media_ids
        )
    )
