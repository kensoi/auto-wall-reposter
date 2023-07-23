"""
Copyright 2023 kensoi
"""

import os

from vkbotkit.objects import callback, Library
from vkbotkit.objects.enums import NameCases
from vkbotkit.objects.filters.filter import Filter, Not
from vkbotkit.objects.filters.message import IsCommand

# Filter helper
init = lambda definition: definition()

# Filters

@init
class isSysAdmin(Filter):
    async def check(self, _, package):
        return package.from_id != int(os.environ.get("BOT_ADMIN_ID"))
    
StopBotRequest = IsCommand({"выход", "stop"}, only_without_args=True)


# Message reaction templates

STOP_REACTION = """
Хорошо, завершаю работу.
"""

ERROR_REACTION = """
{user_mention}, вам нельзя проворачивать такую аферу.
"""


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