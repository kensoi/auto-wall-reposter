"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.filter import Filter, Negation
from vkbotkit.objects.filters.message import IsCommand


class LengthLimit(Filter):
    async def check(self, _, package):
        return len(package.items) == 3
    

SHORTING_NO_ARGS = """
{user_mention}, отправьте команду с ссылкой без пробелов, например "миурува сократить vk.com".
"""

SHORTING_RESULT = """
{user_mention}, ваша ссылка: {link}.
"""

SHORTING_TOO_MANY = """
{user_mention}, невозможно сократить ссылку: в ней содержится один или несколько пробелов.
"""

Request = IsCommand({"сократить", "сократи"}, only_with_args=True)
RequestWithoutLimit = LengthLimit & Request
RequestWithLimit = Negation(LengthLimit) & Request
RequestWithoutLink = IsCommand({"сократить", "сократи"}, only_with_args=False)

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
        
    @callback(RequestWithLimit)
    async def error_message(self, toolkit, package):
        """
        too many args
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        response = SHORTING_TOO_MANY.format(
            user_mention = repr(user_mention)
        )

        await toolkit.messages.send(package, response)

    @callback(RequestWithoutLimit)
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
        
