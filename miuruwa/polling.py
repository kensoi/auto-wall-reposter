"""
Copyright 2023 kensoi
"""

from requests.exceptions import ReadTimeout
from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.callback import callback
from vkbotkit.utils import gen_random

from assets.telegram.api import post_message
from assets.x.api import create_post
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
    def format_post_test(text):
        if len(text) > 128:
            return text[:128] + "..."
        return text

    @callback(NewPost)
    async def repost(self, toolkit, package):
        """
        Repost handler
        """

        post_result = SUCCESS_REPOST
        result_type = LogLevel.DEBUG

        post_id = f"wall{package.owner_id}_{package.id}"
        post_link = f"https://vk.com/{post_id}"

        notification = TELEGRAM_CHANNEL_NOTIFICATION.format(post_link=post_link)

        if package.donut.is_donut:
            notification = TELEGRAM_CHANNEL_NOTIFICATION_DONUT.format(
                post_link=post_link,
                description=self.format_post_test(package.text)
            )

        try:
            await toolkit.api.messages.send(
                random_id = gen_random(),
                peer_id = SysAdminTools.repost_hub,
                attachment = post_id,
                message=VK_CHAT_NOTIFICATION
            )

            if SysAdminTools.is_x_enabled and not package.donut.is_donut:
                await create_post(package.text, package.attachments)

            if SysAdminTools.is_telegram_enabled:
                await post_message(notification.format(post_link=post_link))

        except ReadTimeout as exception:
            post_result = EXCEPTION_MESSAGE.format(exception=exception)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(post_result, log_level=result_type)
            await toolkit.api.messages.send(
                random_id = gen_random(),
                peer_id = SysAdminTools.log_hub,
                message = post_result
            )
