"""
Copyright 2023 kensoi
"""

from vkbotkit.objects.filters.message import IsCommand

SHORTING_START = """
{user_mention}, отправьте в ответ вашу ссылку
"""

SHORTING_RESULT = """
{user_mention}, ваша ссылка: {link}
"""

SHORTING_TOO_MANY = """
{user_mention}, невозможно сократить ссылку: в ней содержится один или несколько пробелов.
"""

Request = IsCommand({"сократить", "сократи"})