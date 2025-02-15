"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases

from .templates import SHORT_LINK_HELP, SHORTING_RESULT
from .filters import ShortLinkArgsTrouble, ShortLinkArgs


class ShortLink(Library):
    """
    Shorting link method
    """

    @callback(ShortLinkArgsTrouble)
    async def help(self, toolkit, package):
        """
        package items limit error reaction
        """

        await toolkit.messages.send(package, SHORT_LINK_HELP)

    @callback(ShortLinkArgs)
    async def short_response(self, toolkit, package):
        """
        shorting process handler
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        link = await toolkit.api.utils.getShortLink(url = package.items[2])
        response = SHORTING_RESULT.format(
            user_mention = repr(user_mention),
            link = link.short_url
        )

        await toolkit.messages.send(package, response)
