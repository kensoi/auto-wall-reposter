"""
Copyright 2022 kensoi
"""
from os import getenv

from vkbotkit.objects import callback, Library
from vkbotkit.objects.filters.actions import ChatInviteUser
from vkbotkit.objects.filters.message import IsThatText, IsCommand

class Hello:
    condition = IsCommand({"старт",}) | IsThatText({"Начать", "начать"}) | ChatInviteUser()
    message = """
Привет, пользователь!

Мы рады вашему вступлению! На сей раз правил нет, но в будущем они могут появиться! Следите за тегом #правила в этой беседе, чтобы узнать больше.
"""

class Help:
    condition = IsCommand({"помощь",}) | IsThatText({"Помощь", "помощь"})
    message = """
#помощь

Правил нет, наслаждайтесь свободой. Пока что.
"""

class Admin:
    condition = IsCommand({"бот-админы",}) | IsThatText({"Кто админ бота", "кто админ бота", "Кто админ бота?", "кто админ бота?"})
    message = """
Пользователь, ботом руководит [id{bot_admin_id}|{bot_admin_name}]
"""

class End:
    condition = IsCommand({"выход",})
    
    class messages:
        ok = """
Хорошо, завершаю работу.
"""
        no_rights = """
У вас нет прав в системе чатбота, чтобы провернуть эту аферу.
"""


class Main(Library):
    """
    Библиотека с командами, предназначенными для приветствия пользователей
    """

    @callback(Hello.condition)
    async def send_hello(self, toolkit, package):
        await toolkit.messages.send(package, Hello.message)


    @callback(Help.condition)
    async def send_help(self, toolkit, package):
        await toolkit.messages.send(package, Help.message)

        
    # @callback(Admin.condition)
    # async def send_admin_list(self, toolkit, package):
    #     bot_admin_id = getenv("BOT_ADMIN_ID")
    #     bot_admin_name = await toolkit.create_mention(mention_id = bot_admin_id)

    #     await toolkit.messages.send(package, Admin.message.format(
    #         bot_admin_id = bot_admin_id,
    #         bot_admin_name = bot_admin_name
    #     ))

        
    @callback(End.condition)
    async def end_bot(self, toolkit, package):
        if package.from_id == int(getenv("BOT_ADMIN_ID")):
            await toolkit.messages.send(package, End.messages.ok)

            quit()

        await toolkit.messages.send(package, End.messages.no_rights)

        

        