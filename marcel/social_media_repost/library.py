"""
Copyright 2023 kensoi
"""

from requests.exceptions import ReadTimeout
from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.callback import callback
from vkbotkit.utils import gen_random

from assets.utils.sys_admin_tools import SysAdminTools

from .filters import NewPost
from .templates import (
    VK_CHAT_NOTIFICATION,
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

        try:
            await toolkit.api.messages.send(
                random_id = gen_random(),
                peer_id = SysAdminTools.repost_chat,
                attachment = post_id,
                message=VK_CHAT_NOTIFICATION
            )

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
