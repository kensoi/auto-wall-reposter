"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.filter import Filter, Not
from vkbotkit.objects.filters.message import IsCommand, IsBotAdmin, IsUserAdmin, IsUserChat

from assets.utils.init import init

@init
class WithMentions(Filter):
    async def check(self, _, package):
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
KickCommand = KickCommand & IsBotAdmin & IsUserAdmin & WithMentions