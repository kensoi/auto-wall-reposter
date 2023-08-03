"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Filter, Not
from vkbotkit.objects.filters.message import IsCommand, IsUserAdmin, IsConversation

from assets.utils.init import init


@init
class WithMentions(Filter):
    """
    Message have 1 or more mentions excluding bot mention
    """

    async def check(self, toolkit, package):
        """
        check function
        """

        if "mentions" not in package.raw or "fwd_messages" not in package.raw:
            return

        mentions_list = set(map(lambda item: item.value, package.mentions))

        if toolkit.bot_is_group:
            equal_list = set([-toolkit.bot_id])
        else:
            equal_list = set([toolkit.bot_id])

        if len(package.mentions) != 0 and \
            mentions_list\
            != equal_list:
            return True

        if len(package.fwd_messages) != 0:
            if len(package.fwd_messages) == 1 and set([package.fwd_messages[0].from_id]) == equal_list:
                return False
            return True

        if "reply_message" in package.raw and set([package.reply_message.from_id]) != equal_list:
            return True

KickCommand = IsCommand(["кик", "кикнуть", "kick"])

NotMultiuserChat = KickCommand & Not(IsConversation)
NoAdminRights = KickCommand & IsConversation & Not(IsUserAdmin)
NoMentions = KickCommand & IsConversation & IsUserAdmin & Not(WithMentions)
AdminKickCommand = KickCommand & IsConversation & IsUserAdmin & WithMentions

AllAdminsCommand = IsCommand(["админы", "администрация", "admin", "admins"], only_without_args=True)
AllBotsCommand = IsCommand(["бот", "боты", "bot", "bots"], only_without_args=True)
AllOnlineCommand = IsCommand(["онлайн", "online"], only_without_args=True)

AllAdminsCommandWRights = AllAdminsCommand
AllBotsCommandWRights = AllBotsCommand
AllOnlineCommandWRights = AllOnlineCommand
