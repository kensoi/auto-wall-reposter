"""
Copyright 2023 kensoi
"""

import os

from aiohttp.client_exceptions import ClientResponseError

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
    """
    Post to telegram via command "{bot_mention} post {message}"
    """

    @callback(TGNoArgs)
    async def no_args(self, toolkit, package):
        """
        try to post without message text or attachments
        """

        response = NO_ARGS_AT_COMMAND.format(
            bot_mention = repr(package.items[0]),
            command = package.items[1]
        )
        await toolkit.messages.send(package, response)

    @callback(TGNotBotAdmin)
    async def unknown_user(self, toolkit, package):
        """
        User has no bot-admin rights
        """

        await toolkit.messages.send(package, USER_IS_NOT_BOT_ADMIN)

    @callback(TGBotAdminPost)
    async def repost(self, toolkit, package):
        """
        User with bot-admin rights send message to post at telegram channel
        """

        result_type = LogLevel.DEBUG
        channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
        channel_notification = " ".join(package.items[2:])
        tweet_result = SUCCESS_REPOST_TELEGRAM.format(channel_id = channel_id)

        try:
            await post_message(channel_notification, package.attachments)

        except ClientResponseError as exception:
            tweet_result = EXCEPTION_MESSAGE.format(exception=exception )
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(tweet_result, log_level=result_type)
            await toolkit.messages.send(package, tweet_result)
