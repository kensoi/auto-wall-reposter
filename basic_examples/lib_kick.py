"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import Library
from vkbotkit.objects.filters.filter import Negation
from vkbotkit.objects.filters.message import IsCommand, IsUserAdmin, IsUserChat, IsBotAdmin
from vkbotkit.objects.callback import callback
from vkbotkit.objects.mention import Mention


NO_ADMIN_RIGHTS = """
У бота нет прав администратора для выполнения этой команды.
"""
NO_ADMIN_RIGHTS_AT_USER = """
У вас нет прав администратора для выполнения этой команды.
"""
ONLY_CHAT_COMMAND = """
Эта команда предназначена для беседы.
"""
KICK_START = """
Исключаю пользователей...
"""
KICK_FINISH = """
Пользователи исключены.
"""
KICK_EXCEPT_NO_USER = """
Нет выделенных пользователей. Для выделения пользователей отправьте команду "@canarybot кик" со списком упоминаний в любой форме, списком пересланных сообщений или ответом на сообщение.
"""
KICK_EXCEPT_ADMIN = """
Невозможно исключить {}: пользователь имеет права администратора.
"""
KICK_EXCEPT_NO_MEMBER = """
Невозможно исключить {}: не состоит в беседе.
"""


class Main(Library):
    """
    Плагин для управления беседой при помощи VKBotKit
    Команды в этом плагине:
    @botname кик
    """

    @callback(IsCommand({"кик", "исключить", "выкинуть"}) & IsUserChat())
    async def sozyv_user(self, toolkit, package):
        """
        при получении команды '@botname созвать' в диалоге => отправлять текст ONLY_CHAT_COMMAND
        """

        await toolkit.messages.send(package, ONLY_CHAT_COMMAND)


    @callback(IsCommand({"кик", "исключить", "выкинуть"}) & Negation(IsBotAdmin()))
    async def sozyv_no_bot_admin(self, toolkit, package):
        """
        при получении команды '@botname созвать' при отсутствии
        прав админа у бота => отправлять текст NO_ADMIN_RIGHTS
        """

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS)


    @callback(IsCommand({"кик", "исключить", "выкинуть"}) & IsBotAdmin() & Negation(IsUserAdmin()))
    async def sozyv_no_admin(self, toolkit, package):
        """
        при получении команды '@botname созвать' при отсутствии
        прав админа у пользователя => отправлять текст NO_ADMIN_RIGHTS_AT_USER
        """

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS_AT_USER)


    @callback(IsCommand({"кик", "исключить", "выкинуть"}) & IsBotAdmin() & IsUserAdmin())
    async def sozyv_admin(self, toolkit, package):
        """
        Функция для исключения пользователей
        """

        user_map = []

        if hasattr(package, "fwd_messages"):
            fwd_messages = map(lambda message: message.from_id, package.fwd_messages)
            user_map.extend(fwd_messages)

        if hasattr(package, "reply_message"):
            user_map.append(package.reply_message.from_id)

        if len(user_map) == 0:
            await toolkit.messages.send(package, KICK_EXCEPT_NO_USER)

        else:
            user_list = await toolkit.get_chat_members(package.peer_id)
            admin_list = await toolkit.get_chat_admins(package.peer_id)

            await toolkit.messages.send(package, KICK_START)

            for i in user_map:
                mention = Mention(i)

                if i in user_list:
                    if i in admin_list:
                        await toolkit.messages.send(
                            package,
                            KICK_EXCEPT_ADMIN.format(mention.repr)
                            )

                    else:
                        await toolkit.api.messages.removeChatUser(
                            chat_id = package.peer_id - 2000000000,
                            user_id = i
                        )
                else:
                    await toolkit.messages.send(
                        package,
                        KICK_EXCEPT_NO_MEMBER.format(mention)
                        )
