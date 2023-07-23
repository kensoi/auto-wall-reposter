"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.mention import Mention
from vkbotkit.objects.enums import NameCases

from vkbotkit.objects.filters.filter import Not
from vkbotkit.objects.filters.message import IsCommand, IsUserAdmin, IsUserChat, IsBotAdmin


Command = IsCommand({"кик", "исключить", "выкинуть"})

NO_ADMIN_RIGHTS = """
{user_mention}, у меня нет прав администратора для выполнения этой команды.
"""

NO_ADMIN_RIGHTS_AT_USER = """
{user_mention}, вам нельзя проворачивать такую аферу.
"""

ONLY_CHAT_COMMAND = """
{user_mention}, эта команда предназначена для беседы.
"""

KICK_START = """
{user_mention}, исключаю пользователей...
"""

KICK_FINISH = """
Пользователи исключены.
"""

KICK_EXCEPT_NO_USER = """
Нет выделенных пользователей. Для выделения пользователей отправьте команду "{bot_mention} кик" со списком упоминаний в любой форме, списком пересланных сообщений или ответом на сообщение.
"""

KICK_EXCEPT_ADMIN = """
Невозможно исключить {}: пользователь имеет права администратора.
"""

KICK_EXCEPT_NO_MEMBER = """
Невозможно исключить {}: не состоит в беседе.
"""

class Main(Library):
    """
    Kick user via command
    """

    @callback(Command & IsUserChat)
    async def kick_user(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, ONLY_CHAT_COMMAND.format(
            user_mention = repr(user_mention)
        ))


    @callback(Command & Not(IsBotAdmin))
    async def kick_no_bot_admin(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS.format(
            user_mention = repr(user_mention)
        ))


    @callback(Command & IsBotAdmin & Not(IsUserAdmin))
    async def kick_no_admin(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS_AT_USER.format(
            user_mention = repr(user_mention)
        ))


    @callback(Command & IsBotAdmin & IsUserAdmin)
    async def kick_admin(self, toolkit, package):
        user_map = package.mentions[1:]

        if hasattr(package, "fwd_messages"):
            fwd_messages = map(lambda message: message.from_id, package.fwd_messages)
            user_map.extend(fwd_messages)

        if hasattr(package, "reply_message"):
            user_map.append(package.reply_message.from_id)

        if len(user_map) == 0:
            bot_mention = await toolkit.get_my_mention()

            await toolkit.messages.send(package, KICK_EXCEPT_NO_USER.format(
                bot_mention = repr(bot_mention)
            ))

        else:
            user_list = await toolkit.get_chat_members(package.peer_id)
            admin_list = await toolkit.get_chat_admins(package.peer_id)

            user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
            
            await toolkit.messages.send(package, KICK_START.format(
                user_mention = repr(user_mention)
            ))

            for i in set(user_map):
                mention = Mention(i) if type(i) != Mention else i

                if i in user_list:
                    if i in admin_list:
                        await toolkit.messages.send(
                            package,
                            KICK_EXCEPT_ADMIN.format(repr(mention))
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