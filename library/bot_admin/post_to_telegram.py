"""
Copyright 2023 kensoi
"""

import os

from aiohttp.client_exceptions import ClientResponseError

from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.callback import callback

from assets.telegram.api import post_message
from assets.utils.sys_admin_tools import SysAdminTools

from .filters import (
    TGBotAdminPost,
    TGNotBotAdmin,
    TGNoArgs
)
from .templates import (
    NO_ARGS_AT_COMMAND,
    USER_IS_NOT_BOT_ADMIN,
    SUCCESS_REPOST_TELEGRAM,
    EXCEPTION_MESSAGE,
    TABOO_REPOST
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

        if not SysAdminTools.is_telegram_enabled:
            return await toolkit.messages.send(package, TABOO_REPOST)

        result_type = LogLevel.DEBUG
        channel_notification = " ".join(package.items[2:])
        send_result = SUCCESS_REPOST_TELEGRAM.format(channel_id = channel_id)

        try:
            await post_message(channel_notification, package.attachments)
            channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")

        except ClientResponseError as exception:
            send_result = EXCEPTION_MESSAGE.format(exception=exception )
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(send_result, log_level=result_type)
            await toolkit.messages.send(package, send_result)
