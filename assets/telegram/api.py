"""
Copyright 2023 kensoi
"""

import asyncio
import json
import os
import typing

import aiohttp

from assets.utils.init import init


@init
class Client:
    """
    telegram client
    """

    def __init__(self):
        """
        init method
        """

        self.session = aiohttp.ClientSession()

    @property
    def api(self):
        """
        api link
        """

        return "https://api.telegram.org/bot{access_token}/{method_name}"

    async def post(self,
                   chat_id:typing.Union[str, int],
                   message:typing.Optional[str]=None,
                   photo_list:typing.Optional[list[str]]=None
                ):
        """
        HTTP POST METHOD
        """

        if not message:
            message = ""

        if not photo_list:
            photo_list = []

        method_data = {}
        method_data["chat_id"] = chat_id

        if len(photo_list) <= 1:
            if len(photo_list) == 0:
                method_name = "sendMessage"
                text_key = "text"

            elif len(photo_list) == 1:
                method_name = "sendPhoto"
                text_key = "caption"
                method_data["photo"] = photo_list[0]

            method_data[text_key] = message

            method = self.api.format(
                access_token = os.environ.get("TELEGRAM_BOT_TOKEN"),
                method_name = method_name
            )

            return await self.session.post(url=method, data=method_data)

        method = self.api.format(
            access_token = os.environ.get("TELEGRAM_BOT_TOKEN"),
            method_name = "sendMediaGroup"
        )
        media_list = list(map(get_input_media_photo, photo_list))

        method_data["media"] = json.dumps(media_list)

        await self.session.post(url=method, data=method_data)

        method = self.api.format(
            access_token = os.environ.get("TELEGRAM_BOT_TOKEN"),
            method_name = "sendMessage"
        )

        method_data.pop("media")
        method_data["text"] = message

        return await self.session.post(url=method, data=method_data)

def get_input_media_photo(photo_url: str):
    """
    get inputmediaphoto object
    """

    return {
        "type": "photo",
        "media": photo_url,
    }

async def get_photo_url(photo):
    """Upload photos on Telegram server

    ### Args:
        photo: object of VK Photo
    """

    return max(photo.photo.sizes, key=lambda photo: photo.height).url

async def post_message(message: typing.Optional[str]=None, attachments: typing.Optional[list]=None):
    """Posts message on telegram channel that is specified by .env. 

    ### Args:
        message: message to post.
        attachments: list of vk photo objects [optional]
    """

    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")

    if len(attachments) == 0:
        await Client.post(channel_id, message)
        return

    photo_attachments = list(filter(
        lambda item: item.type == "photo", attachments
    ))

    list_of_photos = await asyncio.gather(*map(get_photo_url, photo_attachments))

    await Client.post(channel_id, message, list_of_photos)
