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
Привет, пользователь! Мы рады вашему вступлению! 
Чтобы получить список команд для бота, напишите "{bot_mention} команды"
"""

class Rules:
    condition = IsCommand({"правила",})
    message = """
#правила
Правила не установлены.
"""

class Commands:
    condition = IsCommand({"команды", "помощь",}) | IsThatText({"Помощь", "помощь"})
    message = """
Список команд:

{bot_mention} помощь - вызвать краткую информацию по пользованию чат-ботом
{bot_mention} команды - получить список команд для чат-бота.
{bot_mention} правила - получить список правил беседы "Миурува на каждый день"
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
        bot_mention = await toolkit.get_my_mention()
        await toolkit.messages.send(package, Hello.message.format(
            bot_mention = repr(bot_mention)
        ))


    @callback(Rules.condition)
    async def send_rules(self, toolkit, package):
        await toolkit.messages.send(package, Rules.message)
        

    @callback(Commands.condition)
    async def send_commands(self, toolkit, package):
        bot_mention = await toolkit.get_my_mention()
        await toolkit.messages.send(package, Commands.message.format(
            bot_mention = repr(bot_mention)
        ))
        
    @callback(End.condition)
    async def end_bot(self, toolkit, package):
        if package.from_id == int(getenv("BOT_ADMIN_ID")):
            await toolkit.messages.send(package, End.messages.ok)

            quit()

        await toolkit.messages.send(package, End.messages.no_rights)

        

        