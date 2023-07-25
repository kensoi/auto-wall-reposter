"""
Copyright 2023 kensoi
"""

import asyncio
import os
import tweepy

from concurrent.futures import ThreadPoolExecutor
from io import BytesIO


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
