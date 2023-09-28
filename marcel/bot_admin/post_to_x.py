"""
Copyright 2023 kensoi
"""

from requests.exceptions import ReadTimeout
from vkbotkit.objects import Library
from vkbotkit.objects.enums import LogLevel, NameCases
from vkbotkit.objects.callback import callback

from assets.x.api import post_on_x
from assets.utils.sys_admin_tools import SysAdminTools

from .filters import (
    XBotAdminPost,
    XNotBotAdmin,
    XNoArgs
)
from .templates import (
    NO_ARGS_AT_COMMAND,
    USER_IS_NOT_BOT_ADMIN,
    SUCCESS_REPOST_TWITTER,
    EXCEPTION_MESSAGE,
    TABOO_REPOST
)


class XPost(Library):
    """
    Send post to X
    """

    @callback(XNoArgs)
    async def no_args(self, toolkit, package):
        """
        try to post without message text or attachments
        """

        response = NO_ARGS_AT_COMMAND.format(
            bot_mention = package.items[0],
            command = package.items[1]
        )

        await toolkit.messages.send(package, response)

    @callback(XNotBotAdmin)
    async def unknown_user(self, toolkit, package):
        """
        User has no bot-admin rights
        """

        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)
        response = USER_IS_NOT_BOT_ADMIN.format(user_mention=user_mention)

        await toolkit.messages.send(package, response)

    @callback(XBotAdminPost)
    async def repost(self, toolkit, package):
        """
        User with bot-admin rights sent command to post
        """

        if not SysAdminTools.is_x_enabled:
            return await toolkit.messages.send(package, TABOO_REPOST)

        result_type = LogLevel.DEBUG
        post_result = SUCCESS_REPOST_TWITTER
        channel_notification = " ".join(package.items[2:])

        try:
            await post_on_x(channel_notification, package.attachments)

        except ReadTimeout as exception:
            post_result = EXCEPTION_MESSAGE.format(exception=exception)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(post_result, log_level=result_type)
            await toolkit.messages.send(package, post_result)
