"""
copyright 2025 miuruwa
"""

import os

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.exceptions import MethodError

from .filters import (
    NoAdminRights, NoMentions, AdminKickCommand
)
from .templates import (
    NO_ADMIN_RIGHTS,
    NO_BOT_ADMIN_RIGHTS,
    NO_MENTIONS,
    KICK_PROCESS_START,
    KICK_FAIL_USER_ADMIN,
    KICK_FAIL_USER_NOT_EXIST,
    KICK_PROCESS_END
)


class KickUsers(Library):
    """
    Admin kick users
    """

    async def no_bot_rights(self, toolkit, package):
        """
        bot has not admin rights
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        link = os.environ.get("INSTALL_GUIDE_LINK")

        response = NO_BOT_ADMIN_RIGHTS.format(
            user_mention = user_mention,
            link = link
        )

        return await toolkit.messages.send(package, response)

    def get_users_to_kick(self, package):
        """
        generator that yield a list of mentioned users in message (excluding bot)
        """

        yield from map(int, package.mentions[1:])

        if "fwd_messages" in package.raw:
            yield from map(lambda message: message.from_id, package.fwd_messages)

        if "reply_message" in package.raw:
            yield package.reply_message.from_id

    async def kick_user(self, toolkit, peer_id, user_id):
        """
        Kick method
        """

        chat_id = peer_id - 2000000000

        return await toolkit.api.messages.removeChatUser(
            chat_id = chat_id,
            user_id = user_id
        )

    @callback(NoAdminRights)
    async def no_admin_rights(self, toolkit, package):
        """
        User has no rights to kick
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        response = NO_ADMIN_RIGHTS.format(
            user_mention = user_mention
        )

        await toolkit.messages.send(package, response)

    @callback(NoMentions)
    async def no_mentions(self, toolkit, package):
        """
        Command without mentions
        """
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        response = NO_MENTIONS.format(
            user_mention = repr(user_mention)
        )

        await toolkit.messages.send(package, response)


    @callback(AdminKickCommand)
    async def kick_process(self, toolkit, package):
        """
        Processing kick of users that mentioned in command message
        """


        try:
            user_list = await toolkit.get_chat_members(package.peer_id)
            admin_list = await toolkit.get_chat_admins(package.peer_id)

        except MethodError:
            return await self.no_bot_rights(toolkit, package)

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        response = KICK_PROCESS_START.format(user_mention = user_mention)
        await toolkit.messages.send(package, response)

        for user_id in self.get_users_to_kick(package):
            if user_id in user_list and user_id not in admin_list:
                await self.kick_user(toolkit, package.peer_id, user_id)

            user_parent = await toolkit.create_mention(user_id, None, NameCases.GEN)

            if user_id not in user_list:
                response = KICK_FAIL_USER_NOT_EXIST.format(user_parent=user_parent)
                await toolkit.messages.send(package, response)

            if user_id in admin_list:
                response = KICK_FAIL_USER_ADMIN.format(user_parent=user_parent)
                await toolkit.messages.send(package, response)

        await toolkit.messages.send(package, KICK_PROCESS_END)
