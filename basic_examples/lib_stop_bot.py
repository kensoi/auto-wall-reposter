"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.filters.filter import Filter, Negation
from vkbotkit.objects.filters.message import IsCommand


END_POLLING = """
Завершаю прослушку сервера.
"""
NO_END_POLLING = """
Не могу завершить прослушку, так как вы не являетесь создателем
"""


class OwnerId(Filter):
    """
    Закрывает создатель бота, или это посторонний человек
    """

    async def check(self, _, package):
        return package.from_id == 1


class Main(Library):
    """
    Плагин для управления беседой при помощи VKBotKit
    Команды в этом плагине:
    @botname стоп
    """


    @callback(IsCommand({"стоп", "остановить"}) & OwnerId())
    async def end_owner(self, toolkit, package):
        """
        при получении команды '@kyokoubot стоп' => выключать бота
        """

        await toolkit.messages.send(package, END_POLLING)
        toolkit.stop_polling()


    @callback(IsCommand({"стоп", "остановить"}) & Negation(OwnerId()))
    async def end_not_owner(self, toolkit, package):
        """
        при получении команды '@kyokoubot стоп' => выключать бота
        """

        await toolkit.messages.send(package, NO_END_POLLING)
        toolkit.stop_polling()
