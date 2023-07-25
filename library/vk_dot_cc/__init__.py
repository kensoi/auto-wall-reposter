"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.filter import Not

from .filters import *
from .templates import *

class Main(Library):
    """
    Get short link by vk.cc
    """

    @callback(RequestWithoutLink)
    async def help_message(self, toolkit, package):
        """
        No args
        """
        
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, SHORTING_NO_ARGS.format(
                user_mention = repr(user_mention)
            ))
        
    @callback(Not(LengthLimit) & Request)
    async def error_message(self, toolkit, package):
        """
        too many args
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        response = SHORTING_TOO_MANY.format(
            user_mention = repr(user_mention)
        )

        await toolkit.messages.send(package, response)

    @callback(LengthLimit & Request)
    async def answer(self, toolkit, package):
        """
        short link
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        link = await toolkit.api.utils.getShortLink(url = package.items[2])

        response = SHORTING_RESULT.format(
            user_mention = repr(user_mention), 
            link = link.short_url
        )

        await toolkit.messages.send(package, response)
        
