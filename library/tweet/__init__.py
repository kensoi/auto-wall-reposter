"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import callback, Library

from vkbotkit.objects.filters.filter import Filter, Not
from vkbotkit.objects.filters.events import WhichEvent
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.enums import Events, LogLevel

from .api import tweet
from .templates import *
from .filters import *

class Main(Library):
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


    @callback(NotAdmin)
    async def taboo(self, toolkit, package):
        await toolkit.messages.send(package, RIGHTS_ERROR)


    @callback(TweetTrouble)
    async def tweet_help(self, toolkit, package):
        """
        Send help message to user
        """
        
        bot_mention = await toolkit.get_my_mention()

        await toolkit.messages.send(package, NO_MESSAGE.format(bot_mention = repr(bot_mention)))
    

    @callback(MessageToTweet)
    async def tweet(self, toolkit, package):
        try:
            message_to_tweet = " ".join(package.items[2:])
            await tweet(toolkit, message_to_tweet, package.attachments)

            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)
            await toolkit.messages.send(package, NO_ERRORS)

        except Exception as e:
            toolkit.log(EXCEPTION_MESSAGE.format(exception=e), log_level=LogLevel.ERROR)
            await toolkit.messages.send(package, EXCEPTION_MESSAGE.format(exception=e))
