"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import callback, Library

from vkbotkit.objects.enums import LogLevel

from .api import tweet
from .templates import NO_ERRORS, EXCEPTION_MESSAGE
from .filters import PostToTweet


class Reposter(Library):
    """
    Twitter API library for VKBotKit
    """

    @callback(PostToTweet)
    async def repost(self, toolkit, package):
        """
        Tweet with post data (message & photos)
        """
        
        try:
            await tweet(toolkit, package.text, package.attachments)
            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)