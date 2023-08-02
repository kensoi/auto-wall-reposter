"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Filter, Not
from vkbotkit.objects.filters.message import IsCommand, IsUserAdmin, IsUserChat

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
NoAdminRights = KickCommand & IsUserChat & Not(IsUserAdmin)
NoMentions = KickCommand & IsUserChat & IsUserAdmin & Not(WithMentions)
AdminKickCommand = KickCommand & IsUserAdmin & WithMentions

AllAdminsCommand = IsCommand(["админы", "администрация", "admin", "admins"], only_without_args=True)
AllBotsCommand = IsCommand(["бот", "боты", "bot", "bots"], only_without_args=True)
AllOnlineCommand = IsCommand(["онлайн", "online"], only_without_args=True)

AllAdminsCommandWRights = AllAdminsCommand
AllBotsCommandWRights = AllBotsCommand
AllOnlineCommandWRights = AllOnlineCommand
