"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.exceptions import MethodError

from .templates import (
    USER_POINT,
    ADMIN_LIST_TEMPLATE,
    BOT_LIST_TEMPLATE,
    ONLINE_LIST_TEMPLATE,
    NO_BOT_ADMIN_RIGHTS
)
from .filters import (
    AllAdminsCommand, AllBotsCommand, AllOnlineCommand,
)


class ChatData(Library):
    """
    Chat basic info
    """

    async def no_bot_rights(self, toolkit, package):
        """
        bot has not admin rights
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        link = os.environ.get("INSTALL_BOT_ADMIN_RIGHTS")

        response = NO_BOT_ADMIN_RIGHTS.format(
            user_mention = user_mention,
            link = link
        )

        return await toolkit.messages.send(package, response)

    async def get_online_list(self, toolkit, peer_id):
        """
        get screen_names of users that is online right now
        """

        member_list = await toolkit.get_chat_members(peer_id)
        user_list = filter(lambda user_id: user_id > 0, member_list)
        user_ids = ", ".join(map(str, user_list))
        user_data = await toolkit.api.users.get(user_ids = user_ids, fields="online, screen_name")
        online_list = filter(lambda item: item.online == 1, user_data)

        return map(lambda item: item.screen_name, online_list)

    async def get_user_admin_list(self, toolkit, peer_id):
        """
        get screen_names of users that have admin rights in peer_id chat
        """

        admin_list = await toolkit.get_chat_admins(peer_id)
        user_list = filter(lambda user_id: user_id > 0, admin_list)
        user_ids = ", ".join(map(str, user_list))
        user_data = await toolkit.api.users.get(user_ids = user_ids, fields="screen_name")

        return map(lambda item: item.screen_name, user_data)

    async def get_bots_list(self, toolkit, peer_id):
        """
        get screen_names of bots in specified chat 
        """

        admin_list = await toolkit.get_chat_admins(peer_id)
        community_list = filter(lambda user_id: user_id < 0, admin_list)
        group_ids = ", ".join(map(str, community_list))
        community_data = await toolkit.api.groups.getById(
            group_ids = group_ids
        )

        return map(lambda item: item.screen_name, community_data.groups)

    def parse_list(self, iterable):
        """
        format list by template
        """

        return "".join(map(lambda item: USER_POINT.format(screen_name = item), iterable))

    @callback(AllAdminsCommand)
    async def admin_list_reaction(self, toolkit, package):
        """
        send list of admins at specified chat
        """

        try:
            user_list = await self.get_user_admin_list(toolkit, package.peer_id)
        except MethodError:
            return await self.no_bot_rights(toolkit, package)

        parsed_list = self.parse_list(user_list)
        response = ADMIN_LIST_TEMPLATE.format(parsed_list=parsed_list)

        await toolkit.messages.send(package, response)

    @callback(AllBotsCommand)
    async def bot_list_reaction(self, toolkit, package):
        """
        send list of bot at specified chat
        """

        try:
            community_list = await self.get_bots_list(toolkit, package.peer_id)
        except MethodError:
            return await self.no_bot_rights(toolkit, package)

        parsed_list = self.parse_list(community_list)
        response = BOT_LIST_TEMPLATE.format(parsed_list=parsed_list)

        await toolkit.messages.send(package, response)

    @callback(AllOnlineCommand)
    async def bot_online_reaction(self, toolkit, package):
        """
        send list of users on line at specified chat
        """
        try:
            online_list = await self.get_online_list(toolkit, package.peer_id)
        except MethodError:
            return await self.no_bot_rights(toolkit, package)

        parsed_list = self.parse_list(online_list)
        response = ONLINE_LIST_TEMPLATE.format(parsed_list=parsed_list)

        await toolkit.messages.send(package, response)
