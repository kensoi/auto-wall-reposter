"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.callback import callback

from assets.telegram.api import post_message

from .filters import (
    TGBotAdminPost,
    TGNotBotAdmin,
    TGNoArgs
)
from .templates import (
    NO_ARGS_AT_COMMAND,
    USER_IS_NOT_BOT_ADMIN,
    SUCCESS_REPOST_TELEGRAM,
    EXCEPTION_MESSAGE
)


class TelegramPost(Library):
    @callback(TGNoArgs)
    async def no_args(self, toolkit, package):
        with NO_ARGS_AT_COMMAND.format(
            bot_mention = repr(package.items[0]),
            command = package.items[1]
        ) as response:
            await toolkit.messages.send(package, response)

    @callback(TGNotBotAdmin)
    async def unknown_user(self, toolkit, package):
        await toolkit.messages.send(package, USER_IS_NOT_BOT_ADMIN)

    @callback(TGBotAdminPost)
    async def repost(self, toolkit, package):
        tweet_result = SUCCESS_REPOST_TELEGRAM.format(
            channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
        )
        result_type = LogLevel.DEBUG

        channel_notification = " ".join(package.items[2:])
        
        try:
            await post_message(channel_notification, package.attachments)

        except Exception as e:
            tweet_result = EXCEPTION_MESSAGE.format(exception=e)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(tweet_result, log_level=result_type)
            await toolkit.messages.send(package, tweet_result)
