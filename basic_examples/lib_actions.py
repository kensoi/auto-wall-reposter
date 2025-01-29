"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import callback, Library
from vkbotkit.objects.filters.actions import *


class Main(Library):
    """
    Реакции на различные actions в беседе
    """

    @callback(ChatPhotoUpdate())
    async def chat_photo_update(self, toolkit, package):
        """
        Реакция на изменение обложки
        """
        await toolkit.messages.send(package, "ChatPhotoUpdate")


    @callback(ChatPhotoRemove())
    async def chat_photo_remove(self, toolkit, package):
        """
        Реакция на удаление обложки
        """
        await toolkit.messages.send(package, "ChatPhotoRemove")


    @callback(ChatCreate())
    async def chat_create(self, toolkit, package):
        """
        Реакция на создание чата
        """
        await toolkit.messages.send(package, "ChatCreate")


    @callback(ChatTitleUpdate())
    async def chat_title_update(self, toolkit, package):
        """
        Реакция на изменение названия чата
        """
        await toolkit.messages.send(package, "ChatTitleUpdate")


    @callback(ChatInviteUser())
    async def chat_invite_user(self, toolkit, package):
        """
        Реакция на приглашение
        """
        await toolkit.messages.send(package, "ChatInviteUser")


    @callback(ChatInviteUserByLink())
    async def chat_invite_user_by_link(self, toolkit, package):
        """
        Реакция на приглашение
        """
        await toolkit.messages.send(package, "ChatInviteUserByLink")


    @callback(ChatKickUser())
    async def chat_kick_user(self, toolkit, package):
        """
        Реакция на исключение
        """
        await toolkit.messages.send(package, "ChatKickUser")

    @callback(ChatPinMessage())
    async def chat_pin_message(self, toolkit, package):
        """
        Реакция на прикрепление сообщения
        """
        await toolkit.messages.send(package, "ChatPinMessage")

    @callback(ChatUnpinMessage())
    async def chat_unpin_message(self, toolkit, package):
        """
        Реакция на открепление сообщения
        """
        await toolkit.messages.send(package, "ChatUnpinMessage")
