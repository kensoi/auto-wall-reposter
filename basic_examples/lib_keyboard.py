"""
copyright 2025 miuruwa
"""

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.objects.keyboard import Keyboard, KeyboardColor

# важное замечание для клавиатуры
# для работы этого плагина необходимо включить возможности чат-ботов
# vk.com/your_bot_id?act=messages&tab=bots

keyboard_test = Keyboard(one_time = False, inline = True)

keyboard_test.add_button("Кнопка 1", KeyboardColor.PRIMARY)
keyboard_test.add_button("A")
keyboard_test.add_button("B")
keyboard_test.add_line()
keyboard_test.add_button("Кнопка 2", KeyboardColor.PRIMARY)
keyboard_test.add_button("C")
keyboard_test.add_button("D")


class Main(Library):
    """
    Пример плагина с клавиатурой
    """

    @callback(IsCommand({"keyboard", "клавиатура"}))
    async def send_keyboard(self, toolkit, package):
        """
        Команда для отправки команды
        """

        await toolkit.messages.send(
            package, "Пример клавиатуры",
            keyboard = keyboard_test.get_keyboard())
