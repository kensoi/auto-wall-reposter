"""
Copyright 2022 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.message import IsCommand


SHORTING_START = """
{mention}, отправьте в ответ вашу ссылку
"""
SHORTING_RESULT = """
{mention}, ваша ссылка: {link}
"""

SHORTING_TOO_MANY = """
{mention}, невозможно сократить ссылку: в ней содержится один или несколько пробелов.
"""


class Main(Library):
    """
    Сокращатель ссылок
    """

    @callback(IsCommand({"сократить", "сократи"}))
    async def get_short(self, toolkit, package):
        """
        при получении команды '@your_bot_id сократить' => запросить ссылку
        и отправить её на сокращение в vk.cc
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        if len(package.items) == 2:
            await toolkit.messages.send(package, SHORTING_START.format(mention = repr(user_mention)))
            reply = await toolkit.messages.get_reply(package)
            links = [reply.text]

        else:
            links = package.items[2:]
        
        if len(links) == 1:
            link = await toolkit.api.utils.getShortLink(url = links[0])
            response = SHORTING_RESULT.format(mention = repr(user_mention), link = link.short_url)

        else:
            response = SHORTING_TOO_MANY.format(mention = repr(user_mention))

        await toolkit.messages.send(package, response)
        
