"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.mention import Mention
from vkbotkit.objects.enums import NameCases

from vkbotkit.objects.filters.filter import Not
from vkbotkit.objects.filters.message import IsUserAdmin, IsUserChat, IsBotAdmin

from .templates import (
    ONLY_CHAT_COMMAND, NO_ADMIN_RIGHTS, NO_ADMIN_RIGHTS_AT_USER, 
    KICK_EXCEPT_NO_USER, KICK_START, KICK_EXCEPT_ADMIN, KICK_EXCEPT_NO_MEMBER
)

from .filters import KickMembers


class KickMethod(Library):
    """
    Kick user via command
    """

    @callback(KickMembers & IsUserChat)
    async def kick_user(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, ONLY_CHAT_COMMAND.format(
            user_mention = repr(user_mention)
        ))


    @callback(KickMembers & Not(IsBotAdmin))
    async def kick_no_bot_admin(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS.format(
            user_mention = repr(user_mention)
        ))


    @callback(KickMembers & IsBotAdmin & Not(IsUserAdmin))
    async def kick_no_admin(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, NO_ADMIN_RIGHTS_AT_USER.format(
            user_mention = repr(user_mention)
        ))


    @callback(KickMembers & IsBotAdmin & IsUserAdmin)
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