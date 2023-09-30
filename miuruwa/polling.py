"""
Copyright 2023 kensoi
"""

from requests.exceptions import ReadTimeout
from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.enums import LogLevel
from vkbotkit.objects.package import Package
from vkbotkit.utils import gen_random

from assets.telegram.api import post_on_telegram
from assets.x.api import post_on_x
from assets.utils.sys_admin_tools import SysAdminTools

from .filters import NewPost
from .templates import (
    VK_CHAT_NOTIFICATION,
    TELEGRAM_CHANNEL_NOTIFICATION,
    TELEGRAM_CHANNEL_NOTIFICATION_DONUT,
    SUCCESS_REPOST,
    EXCEPTION_MESSAGE,
    X_POST_EDIT_NOTIFY,
    X_POST_EDIT_SUGGESTION,
    X_POST_EDIT_AWAIT,
    X_POST_EDIT_SUCCESS,
    X_POST_EDIT_CANCEL,
    X_POST_KEYBOARD_NO,
    X_POST_KEYBOARD_CANCEL,
)
from .keyboard import (
    get_keyboard_cancel,
    get_keyboard_suggest
)


class Reposter(Library):
    """
    Lib that reposts new post to X and Telegram
    """

    async def telegram_post(self, message):
        """
        Post on telegram
        """

        if SysAdminTools.is_telegram_enabled:
            await post_on_telegram(message)

    async def x_post(self, toolkit, package, post_id):
        """
        Post on x
        """

        if not SysAdminTools.is_x_enabled:
            return

        if package.donut.is_donut:
            return

        response = await self.x_post_edit_suggest(toolkit, post_id)

        await post_on_x(response or package.text, package.attachments)

    async def x_post_edit_suggest(self, toolkit, post_id):
        """
        Suggest new text for post
        """

        keyboard_to_suggest = get_keyboard_suggest()
        keyboard_to_cancel = get_keyboard_cancel()

        suggestor_id = 517114114
        suggestor_package = Package({
            "peer_id": suggestor_id,
            "from_id": suggestor_id
        })

        await toolkit.api.messages.send(
            random_id = gen_random(),
            peer_id = suggestor_id,
            message = X_POST_EDIT_NOTIFY,
            attachment = post_id
        )

        await toolkit.api.messages.send(
            random_id = gen_random(),
            peer_id = suggestor_id,
            message = X_POST_EDIT_SUGGESTION,
            keyboard = keyboard_to_suggest.get_keyboard()
        )

        suggestion_reply = await toolkit.messages.get_reply(suggestor_package)

        if suggestion_reply.text == X_POST_KEYBOARD_NO:
            await toolkit.messages.send(suggestor_package, X_POST_EDIT_CANCEL)
            return None

        await toolkit.api.messages.send(
            random_id = gen_random(),
            peer_id = suggestor_id,
            message = X_POST_EDIT_AWAIT,
            keyboard = keyboard_to_cancel.get_keyboard()
        )

        new_text_reply = await toolkit.messages.get_reply(suggestor_package)

        if new_text_reply.text == X_POST_KEYBOARD_CANCEL:
            await toolkit.messages.send(suggestor_package, X_POST_EDIT_CANCEL)
            return None

        await toolkit.messages.send(suggestor_package, X_POST_EDIT_SUCCESS)
        return new_text_reply.text

    @callback(NewPost)
    async def repost(self, toolkit, package):
        """
        Repost handler
        """

        result_type = LogLevel.DEBUG

        post_id = f"wall{package.owner_id}_{package.id}"
        post_link = f"https://vk.com/{post_id}"

        post_result = SUCCESS_REPOST.format(
            post_original = post_link,
            post_text = package.text
        )
        notification = TELEGRAM_CHANNEL_NOTIFICATION.format(post_link=post_link)

        if package.donut.is_donut:
            notification = TELEGRAM_CHANNEL_NOTIFICATION_DONUT.format(
                post_link=post_link
            )

        try:
            await toolkit.api.messages.send(
                random_id = gen_random(),
                peer_id = SysAdminTools.repost_hub,
                attachment = post_id,
                message=VK_CHAT_NOTIFICATION
            )

            await self.x_post(toolkit, package, post_id)
            await self.telegram_post(notification.format(post_link=post_link))

        except ReadTimeout as exception:
            post_result = EXCEPTION_MESSAGE.format(exception=exception)
            result_type = LogLevel.ERROR

        finally:
            toolkit.log(post_result, log_level=result_type)
            await toolkit.api.messages.send(
                random_id = gen_random(),
                peer_id = SysAdminTools.log_hub,
                message = post_result,
            )
