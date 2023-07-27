"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases

from .templates import SHORT_LINK_HELP, SHORTING_RESULT
from .filters import ShortLinkArgsTrouble, ShortLinkArgs


class ShortLink(Library):
    @callback(ShortLinkArgsTrouble)
    async def help(self, toolkit, package):
        response = SHORT_LINK_HELP.format(
            bot_mention = repr(package.items[0]),
            command = repr(package.items[1]),
        )
        await toolkit.messages.send(package, response)

    @callback(ShortLinkArgs)
    async def short_response(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        link = await toolkit.api.utils.getShortLink(url = package.items[2])

        response = SHORTING_RESULT.format(
            user_mention = repr(user_mention), 
            link = link.short_url
        )

        await toolkit.messages.send(package, response)