"""
copyright 2025 miuruwa
"""

from vkbotkit.objects.keyboard import Keyboard, KeyboardColor

from .templates import (
    X_POST_KEYBOARD_YES,
    X_POST_KEYBOARD_NO,
    X_POST_KEYBOARD_CANCEL
)


def get_keyboard_suggest():
    "Get keyboard"

    keyboard_to_reply = Keyboard(one_time=False, inline=True)

    keyboard_to_reply.add_button(X_POST_KEYBOARD_YES,
        KeyboardColor.POSITIVE, payload={"reaction": "X_POST_KEYBOARD_YES"}
    )
    keyboard_to_reply.add_button(X_POST_KEYBOARD_NO,
        KeyboardColor.NEGATIVE, payload={"reaction": "X_POST_KEYBOARD_NO"}
    )

    return keyboard_to_reply


def get_keyboard_cancel():
    "Get keyboard"

    keyboard_to_reply = Keyboard(one_time=False, inline=True)

    keyboard_to_reply.add_button(X_POST_KEYBOARD_CANCEL,
        KeyboardColor.POSITIVE, payload={"reaction": "X_POST_KEYBOARD_CANCEL"}
    )

    return keyboard_to_reply
