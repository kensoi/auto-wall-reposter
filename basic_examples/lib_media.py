"""
copyright 2025 miuruwa
"""

import asyncio
from os import path
from urllib.parse import urlparse

from vkbotkit.objects import Library
from vkbotkit.objects.callback import callback
from vkbotkit.objects.filters.filter import Filter, Negation
from vkbotkit.objects.filters.message import IsCommand
from vkbotkit.utils import PATH_SEPARATOR

DOWNLOAD_PHOTO_MESSAGE = """
Фотографии сохранены в директории assets/downloads
"""
STICKER_DOWNLOADED = """
Стикер скачан и теперь хранится в директории assets/downloads
"""
NO_PHOTO_MESSAGE = """
К команде необходимо приложить фотографии для скачивания
"""


class HasPhoto(Filter):
    """
    Фильтр для сообщений, содержащих фото
    """

    async def check(self, _, package):
        """
        Проверка условий
        """

        if not package.attachments:
            return

        photos_filter = list(filter(lambda x: x['type'] == 'photo', package.attachments))

        return len(photos_filter) != 0


class StickerFilter(Filter):
    """
    Фильтр для стикеров
    """

    async def check(self, _, package):
        """
        Проверка на наличии стикера в сообщении
        """

        if not hasattr(package, "attachments"):
            return False

        if len(package.attachments) == 0:
            return False

        return package.attachments[0]['type'] == "sticker"



async def download_file(toolkit, download_url):
    """
    Функция для сохранения изображения в папку assets
    """

    file_name = "downloads" + PATH_SEPARATOR + path.basename(urlparse(download_url).path)

    if not file_name.endswith(".jpg"):
        if not file_name.endswith(".png"):
            file_name += ".png"

    async with toolkit._session.get(download_url) as url_content:
        file_content = await url_content.read()

    with toolkit.assets(file_name, 'wb+', encoding=None) as created_file:
        created_file.write(file_content)

    return file_name


class Main(Library):
    """
    Библиотека с примером работы toolkit.assets и toolkit.upload
    """


    @callback(IsCommand({"media", "медиа", "медия"}) & HasPhoto())
    async def download_media(self, toolkit, package):
        """
        Обработчик отправленных пользователем фотографий, который сохраняет
        скачанные фото в папку ассетов
        """

        photos_filtered = filter(lambda x: x['type'] == 'photo', package.attachments)
        photos = list(map(
            lambda x: sorted(x['photo']['sizes'],
            key = lambda j: j['width'])[-1]['url'],
            photos_filtered
        ))

        await asyncio.gather(*[download_file(toolkit, image) for image in photos])
        await toolkit.messages.send(package, DOWNLOAD_PHOTO_MESSAGE)


    @callback(IsCommand({"media", "медиа", "медия"}) & Negation(HasPhoto()))
    async def send_media_help(self, toolkit, package):
        """
        Инструкции к download_media обработчику
        """

        await toolkit.messages.send(package, NO_PHOTO_MESSAGE)


    @callback(StickerFilter())
    async def download_sticker(self, toolkit, package):
        """
        Обработчик отправленных пользователем стикеров, который сохраняет
        скачанные стикеры в папку ассетов
        """

        sticker = package.attachments[0]['sticker']
        filtered = filter(lambda image: image['height'] == 512, sticker['images'])
        result = await download_file(toolkit, list(filtered)[0]['url'])

        await toolkit.messages.send(package, STICKER_DOWNLOADED.format(result))
