"""
Copyright 2022 kensoi
"""

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
    condition = IsCommand({"админы",}) | IsThatText({"Кто админ", "кто админ", "Кто админ?", "кто админ?"})
    message = """
Пользователь, всем в беседе заведует [id517114114|Андрей Прокофьев]
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

        
    @callback(Admin.condition)
    async def send_admin_list(self, toolkit, package):
        await toolkit.messages.send(package, Admin.message)

        
    @callback(End.condition)
    async def end_bot(self, toolkit, package):
        if package.from_id == 517114114:
            await toolkit.messages.send(package, End.messages.ok)

            quit()

        await toolkit.messages.send(package, End.messages.no_rights)

        

        