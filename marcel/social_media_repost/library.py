"""
Copyright 2023 kensoi
"""

from requests.exceptions import ReadTimeout
from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.callback import callback
from vkbotkit.utils import gen_random

from assets.telegram.api import post_message
from assets.twitter.api import tweet
from assets.utils.sys_admin_tools import SysAdminTools

from .filters import NewPost
from .templates import (
    VK_CHAT_NOTIFICATION,
    TELEGRAM_CHANNEL_NOTIFICATION,
    TELEGRAM_CHANNEL_NOTIFICATION_DONUT,
    SUCCESS_REPOST,
    EXCEPTION_MESSAGE
)


class Reposter(Library):
    """
    Lib that reposts new post to X and Telegram
    """

    @callback(NewPost)
    async def repost(self, toolkit, package):
        """
        Repost handler
        """

        tweet_result = SUCCESS_REPOST
        result_type = LogLevel.DEBUG

        post_id = f"wall{package.owner_id}_{package.id}"
        post_link = f"https://vk.com/{post_id}"

        notification = TELEGRAM_CHANNEL_NOTIFICATION

        if package.donut.is_donut:
            notification = TELEGRAM_CHANNEL_NOTIFICATION_DONUT

        try:
            await toolkit.api.messages.send(
                random_id = gen_random(),
                peer_id = SysAdminTools.repost_chat,
                attachment = post_id,
                message=VK_CHAT_NOTIFICATION
            )

            if SysAdminTools.is_x_enabled and not package.donut.is_donut:
                await tweet(toolkit, package.text, package.attachments)

            if SysAdminTools.is_telegram_enabled:
                await post_message(notification.format(post_link=post_link))

        except ReadTimeout as exception:
            tweet_result = EXCEPTION_MESSAGE.format(exception=exception)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(tweet_result, log_level=result_type)
            await toolkit.api.messages.send(
                random_id = gen_random(),
                peer_id = SysAdminTools.log_chat,
                message = tweet_result
            )
