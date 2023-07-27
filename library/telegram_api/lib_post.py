"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback

from .api import post_message

from .templates import RIGHTS_ERROR, NO_MESSAGE, NO_ERRORS, EXCEPTION_MESSAGE
from .filters import MessageToPost, PostTrouble, NotAdmin


class Post(Library):
    """
    Repost a post to specified telegram channel
    """

    @callback(NotAdmin)
    async def taboo(self, toolkit, package):
        await toolkit.messages.send(package, RIGHTS_ERROR)


    @callback(PostTrouble)
    async def post_help(self, toolkit, package):
        """
        Send help message to user
        """
        
        bot_mention = await toolkit.get_my_mention()

        await toolkit.messages.send(package, NO_MESSAGE.format(bot_mention = repr(bot_mention)))
    

    @callback(MessageToPost)
    async def post(self, toolkit, package):
        message_to_post = " ".join(package.items[2:])

        try:
            await post_message(message_to_post)

            toolkit.log(NO_ERRORS, log_level=LogLevel.DEBUG)
            await toolkit.messages.send(package, NO_ERRORS)

        except Exception as e:
            post_result = EXCEPTION_MESSAGE.format(exception=e)

            toolkit.log(post_result, log_level=LogLevel.ERROR)
            await toolkit.messages.send(package, post_result)