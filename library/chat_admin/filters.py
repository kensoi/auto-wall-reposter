"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Filter, Not
from vkbotkit.objects.filters.message import IsCommand, IsBotAdmin, IsUserAdmin, IsUserChat

from assets.utils.init import init


@init
class WithMentions(Filter):
    """
    Message have 1 or more mentions excluding bot mention
    """

    async def check(self, _, package):
        """
        check function
        """

        if "mentions" not in package.raw:
            return

        if len(package.mentions) > 1:
            return True

        if "fwd_messages" in package.raw:
            return True

        if "reply_message" in package.raw:
            return True

        return False

KickCommand = IsCommand(["кик", "кикнуть", "kick"])

NotMultiuserChat = KickCommand & Not(IsUserChat)
NoBotAdminRights = KickCommand & IsUserChat & Not(IsBotAdmin)
NoAdminRights = KickCommand & IsUserChat & IsBotAdmin & Not(IsUserAdmin)
NoMentions = KickCommand & IsUserChat & IsBotAdmin & IsUserAdmin & Not(WithMentions)
AdminKickCommand = KickCommand & IsBotAdmin & IsUserAdmin & WithMentions
