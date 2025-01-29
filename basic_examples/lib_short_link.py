"""
copyright 2025 miuruwa
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


class Main(Library):
    """
    Сокращатель ссылок
    """

    @callback(IsCommand({"сократить"}))
    async def get_short(self, toolkit, package):
        """
        при получении команды '@your_bot_id сократить' => запросить ссылку
        и отправить её на сокращение в vk.cc
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        await toolkit.messages.send(package, SHORTING_START.format(mention = repr(user_mention)))

        reply = await toolkit.messages.get_reply(package)
        link = await toolkit.api.utils.getShortLink(url = reply.text)
        response = SHORTING_RESULT.format(mention = repr(user_mention), link = link.short_url)

        await toolkit.messages.send(package, response)
