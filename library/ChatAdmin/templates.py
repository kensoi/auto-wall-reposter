"""
Copyright 2023 kensoi
"""


NO_ADMIN_RIGHTS = """
{user_mention}, у вас нет прав администратора для этой команды
"""
NO_BOT_ADMIN_RIGHTS = """
{user_mention}, у меня нет прав администратора для выполнения этой команды.
Инструкция по выдаче прав: {link}
"""
NO_MENTIONS = """
{user_mention}, вы не упомянули или не выделили сообщения нужных лиц
"""
KICK_PROCESS_START = """
Начало исключения...
"""
KICK_FAIL_USER_ADMIN = """
Невозможно исключить {user_parent}, так как он имеет права администратора.
"""
KICK_FAIL_USER_NOT_EXIST = """
Невозможно исключить {user_parent}, так как он не состоит в беседе.
"""
KICK_PROCESS_END = """
Исключение завершено
"""
