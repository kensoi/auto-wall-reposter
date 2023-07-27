"""
Copyright 2023 kensoi
"""

REACTION_TO_NEW_USER = """
Привет, {user_mention}! Мы рады вашему вступлению! 
Чтобы получить список команд для бота, напишите "{bot_mention} команды"
"""

REACTION_TO_KICK = """Приносим соболезнования."""

REACTION_WITH_RULES = """
{user_mention}, правила можно найти в соответствующем обсуждении: {topic_link}
"""

REACTION_WITH_COMMANDS = """
{user_mention}, список команд можно найти в соответствующем обсуждении: {topic_link}
"""

STOP_REACTION = """
Хорошо, завершаю работу.
"""

ERROR_REACTION = """
{user_mention}, вам нельзя проворачивать такую аферу.
"""

REACT_THANK = "{reactor_mention}, react.thank"
REACT_SWEAR = "{reactor_mention}, react.swear"

NO_ADMIN_RIGHTS = """
{user_mention}, у меня нет прав администратора для выполнения этой команды.
"""

NO_ADMIN_RIGHTS_AT_USER = """
{user_mention}, вам нельзя проворачивать такую аферу.
"""

ONLY_CHAT_COMMAND = """
{user_mention}, эта команда предназначена для беседы.
"""

KICK_START = """
{user_mention}, исключаю пользователей...
"""

KICK_FINISH = """
Пользователи исключены.
"""

KICK_EXCEPT_NO_USER = """
Нет выделенных пользователей. Для выделения пользователей отправьте команду "{bot_mention} кик" со списком упоминаний в любой форме, списком пересланных сообщений или ответом на сообщение.
"""

KICK_EXCEPT_ADMIN = """
Невозможно исключить {}: пользователь имеет права администратора.
"""

KICK_EXCEPT_NO_MEMBER = """
Невозможно исключить {}: не состоит в беседе.
"""
