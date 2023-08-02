"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.keyboard import Keyboard, KeyboardColor


def get_keyboard_with_actions(user_id):
    """
    get actions for user that send a message
    """

    reaction_keyboard = Keyboard(inline=True)

    reaction_keyboard.add_callback_button(
        "Ответить", KeyboardColor.POSITIVE, 
        payload={
            "from_id": user_id,
            "type": "answer_to_user"
        })

    return reaction_keyboard.get_keyboard()