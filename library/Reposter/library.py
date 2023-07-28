"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.callback import callback

from assets.telegram.api import post_message
from assets.twitter.api import tweet

from .filters import NewPost
from .templates import (
    TELEGRAM_CHANNEL_NOTIFICATION, 
    SUCCESS_REPOST,
    EXCEPTION_MESSAGE
)


class Reposter(Library):
    @callback(NewPost)
    async def repost(self, toolkit, package):
        tweet_result = SUCCESS_REPOST.format(exception=e)
        result_type = LogLevel.DEBUG

        post_full_id = "wall{owner_id}_{post_id}".format(
            owner_id = package.owner_id,
            post_id = package.id
        )

        post_link = "https://vk.com/{post_id}".format(
            post_id = post_full_id
        )

        try:
            await tweet(toolkit, package.text, package.attachments)
            with TELEGRAM_CHANNEL_NOTIFICATION.format(post_link=post_link) as notification:
                await post_message(notification)

        except Exception as e:
            tweet_result = EXCEPTION_MESSAGE.format(exception=e)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(tweet_result, log_level=result_type)
            await toolkit.messages.send(package, tweet_result)
