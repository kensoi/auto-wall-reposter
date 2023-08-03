"""
Copyright 2023 kensoi
"""

from vkbotkit.objects import Library, callback
from vkbotkit.objects.enums import NameCases
from vkbotkit.utils import gen_random

from .filters import (
    KeyboardReply,
    NewMessageFromPrivate
)
from .templates import (
    NOTIFICATION_NEW_MESSAGE,
    REPLY_COMMAND,
    REPLY_FINISH
)
from .keyboards import get_keyboard_with_actions


class PrivateMessagesNode(Library):
    """
    Node to work with private messages
    """

    @callback(NewMessageFromPrivate)
    async def got_message_from_user(self, toolkit, package):
        """
        got a message from user that is not sys-admin
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.GEN)
        keyboard = get_keyboard_with_actions(package.from_id)

        await toolkit.api.messages.send(
            random_id = gen_random(),
            peer_ids = ", ".join(map(str, UserIsSysAdmin.admin_list)),
            message = NOTIFICATION_NEW_MESSAGE.format(
                from_id = repr(user_mention),
                text = package.text
            ),
            keyboard=keyboard
        )

    @callback(KeyboardReply)
    async def got_keyboard_reply(self, toolkit, package):
        """
        got reply from sysadmin as keyboard button
        """

        # if package.payload.type == "ban_user":

        if package.payload.type == "answer_to_user":
            return await self.answer_to_user(toolkit, package)

    async def answer_to_user(self, toolkit, package):
        """
        got reply from sysadmin as keyboard button "answer to user"
        """

        await toolkit.messages.send(package, REPLY_COMMAND)

        reply = await toolkit.messages.get_reply(package)

        await toolkit.api.messages.send(
            random_id=gen_random(),
            peer_id=package.payload.from_id,
            message=reply.text
        )

        await toolkit.messages.send(package, REPLY_FINISH)
