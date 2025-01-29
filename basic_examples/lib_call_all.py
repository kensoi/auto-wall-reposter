"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import Library
from vkbotkit.objects.filters.filter import Negation
from vkbotkit.objects.filters.message import IsCommand, IsUserAdmin, IsUserChat, IsBotAdmin
from vkbotkit.objects.callback import callback
from vkbotkit.objects.mention import Mention


SOZYV = """
ВНИМАНИЕ, ПОЛЬЗОВАТЕЛИ! 
Обратите внимание на сообщения {sender}!
{members}
"""
NO_ADMIN_RIGHTS = """
У бота нет прав администратора для выполнения этой команды.
"""
NO_ADMIN_RIGHTS_AT_USER = """
У вас нет прав администратора для выполнения этой команды.
"""
ONLY_CHAT_COMMAND = """
Эта команда предназначена для беседы.
"""


class Main(Library):
    """
    Плагин для управления беседой при помощи VKBotKit
    Команды в этом плагине:
    @botname созвать
    """

    @callback(IsCommand({"созвать", "позвать", "созыв"}) & IsUserChat())
    async def sozyv_user(self, toolkit, package):
        """
        при получении команды '@botname созвать' в диалоге => отправлять текст ONLY_CHAT_COMMAND
        """

        await toolkit.messages.send(package, ONLY_CHAT_COMMAND)


    @callback(IsCommand({"созвать", "позвать", "созыв"}) & Negation(IsBotAdmin()))
    async def sozyv_no_bot_admin(self, toolkit, package):
        """
        при получении команды '@botname созвать' при отсутствии
        прав админа у бота => отправлять текст NO_ADMIN_RIGHTS
        """

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS)


    @callback(IsCommand({"созвать", "позвать", "созыв"}) & IsBotAdmin() & Negation(IsUserAdmin()))
    async def sozyv_no_admin(self, toolkit, package):
        """
        при получении команды '@botname созвать' при отсутствии
        прав админа у пользователя => отправлять текст NO_ADMIN_RIGHTS_AT_USER
        """

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS_AT_USER)


    @callback(IsCommand({"созвать", "позвать", "созыв"}) & IsBotAdmin() & IsUserAdmin())
    async def sozyv_admin(self, toolkit, package):
        """
        при получении команды '@botname созвать' => отправлять текст SOZYV
        """

        chat_members = await toolkit.get_chat_members(package.peer_id)
        chat_members.remove(package.from_id)
        chat_members_mapped = map(lambda x: Mention(x, "."), chat_members)
        chat_members_repred = map(repr, chat_members_mapped)
        chat_members = " ".join(list(chat_members_repred))

        user_mention = await toolkit.create_mention(package.from_id)
        response = SOZYV.format(
                sender = repr(user_mention),
                members = chat_members)
        toolkit.messages.send(package, response,
            attachment = "photo-195675828_457242153")
