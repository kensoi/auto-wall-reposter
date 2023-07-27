"""
Copyright 2023 kensoi
"""

import aiohttp
import os

from utils import init


@init
class Client:
    def __init__(self):
        self.__ACCESS_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.session = aiohttp.ClientSession()

    @property
    def api(self):
        return "https://api.telegram.org/bot{access_token}/{method_name}"

    async def post(self, chat_id, message):
        method = self.api.format(
            access_token = self.__ACCESS_TOKEN,
            method_name = "sendMessage"
        )

        method_data = {}
        method_data["chat_id"] = chat_id
        method_data["text"] = message

        await self.session.post(url=method, data=method_data)


async def post_message(message):
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
    await Client.post(channel_id, message)
