# Шаблон рабочего чат-бота VKBotKit

В данном репозитории описан стандартный вид чат-бота, работающего при помощи vkbotkit. Репозиторий можно использовать как шаблон.

## Структура репозитория

* `assets` - каталог с медиафайлами (доступ к файлам реализуется через `toolkit.assets` либо `tools.upload`)
* `library` - каталог со скриптами обработчиков
* `bot.py` - корневой скрипт чатбота (для запуска и конфигурации основных настроек)
* `requirements.txt` - файл с требуемыми библиотеками для работы шаблона
* `.env` - файл с переменными окружения

## Полезные ссылки

* [vkbotkit/vkbotkit](https://github.com/vkbotkit/vkbotkit/tree/v1.2)
* [vkbotkit/examples](https://github.com/vkbotkit/examples/tree/v1.2)

# Установка и настройка бота в вашем сообществе ВКонтакте  

## 0. Создайте сообщество ВКонтакте  

Перейдите во вкладку "Сообщества" на сайте ВКонтакте, или используйте ссылку [vk.com/groups](https://vk.com/groups)  

![Нахождение сообщества](https://github.com/kensoi/pycanarybot/blob/master/img/create_community.png?raw=true)  

## 1. Перейдите в раздел для работы с API  

Перейдите во вкладку "Управление" при помощи первой ссылки в админ-меню вашего сообщества  

![Управление](https://github.com/kensoi/pycanarybot/blob/master/img/management_location.png?raw=true)  

Перейдите во вкладку "Работа с API"

## 2. Создайте токен

В шапке раздела нажмите на "Создать ключ"  

![Ключи API](https://github.com/kensoi/pycanarybot/blob/master/img/api_keys.png?raw=true)  

Выберите необходимые права для вашего токена, затем нажмите "Создать" и подтвердите свою личность.  

![Меню с выбором прав токена](https://github.com/kensoi/pycanarybot/blob/master/img/keys_rights.png?raw=true)  

## 3. Настройте Long Poll сервер

В шапке раздела нажмите "Long Poll API".  
Во вкладке "Настройки" включите пункт "Long Poll API" и выберите нужную версию API.  
Во вкладке "Типы событий" выберите нужные типы, которые будут обрабатываться чат-ботом. Обязательно включите "Входящие сообщения".  

## 4. Клонируйте репозиторий бота к себе на компьютер/сервер

В нашем случае мы будем использовать репозиторий [vkbotkit/template](https://github.com/vkbotkit/template/generate) в качестве шаблона. В результате получается репозиторий `your_name/your_bot`, где `your_name` - ваш никнейм, а `your_bot` - название созданного репозитория.

```bash
git clone https://github.com/your_name/your_bot.git
cd your_bot
git checkout v1.2
pip install -r requirements.txt
```

## 5. Настройка бота

Бот готов к использованию, но перед запуском нужно установить полученный в пункте 2 ключ доступа и ID сообщества. Для этого в репозитории нужно создать файл `.env`

* `PUBLIC_TOKEN` - ключ доступа от сообщества
* `PUBLIC_ID` - ID сообщества

* `DEBUG_TOKEN` - ключ доступа от сообщества в режиме отладки
* `DEBUG_ID` - ID сообщества в режиме отладки

* `DEBUG_MODE` - режим отладки (по умолчанию True)
* `CONFIG_LOG` - конфигурация лога

```
f - вывод лога в файл,
c - вывод лога в консоль
```

## 6. Запуск бота

```bash
python3 bot.py [-d]
```

## 7. Проверка работы чатбота
![Канари-чан](https://sun9-52.userapi.com/s/v1/ig2/5yBG60JVrtlBYspn2YdMG8KRFZBSyyPuKr0nCbpc1Ms8hzv9iHQ5toAxm9kxT3Q0w_YzKVUdqWGEQcOMbQY9xWna.jpg?size=512x249&quality=96&type=album)
