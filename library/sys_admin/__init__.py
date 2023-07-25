"""
Copyright 2023 kensoi
"""


from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.filter import Not

from .filters import *
from .templates import *


class Main(Library):
    """
    System administrator tools
    """
        
    @callback(StopBotRequest & isSysAdmin)
    async def end_bot(self, toolkit, package):
        await toolkit.messages.send(package, STOP_REACTION)
        quit()


    @callback(StopBotRequest & Not(isSysAdmin))
    async def end_bot_error(self, toolkit, package):
        user_mention = await toolkit.create_mention(package.from_id, None, NameCases.NOM)

        await toolkit.messages.send(package, ERROR_REACTION.format(
            user_mention = repr(user_mention),
        ))