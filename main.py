import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_album.lock_middleware import LockAlbumMiddleware
from aiogram_album import AlbumMessage

from dataclasses import dataclass
from database import Database
from coloring import ColoredFormatter
from dotenv import dotenv_values
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

log_format = '[%(asctime)s]:%(levelname)-7s:%(message)s'
time_format = '%H:%M:%S'
formatter = ColoredFormatter(log_format, datefmt=time_format)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel('DEBUG')

DEFAULT_DELAY = 0.6

config = dotenv_values('.env')
dp = Dispatcher()
base = Database()
bot = Bot(config["BOT_TOKEN"])
donors = base.get_all_donors()


def create_media_group(
        caption: str,
        file_types: list[str],
        file_ids: list[str]) -> list[InputMediaAudio
                                     | InputMediaPhoto
                                     | InputMediaVideo
                                     | InputMediaDocument]:
    media_group = MediaGroupBuilder(caption=caption)
    for file_id in file_ids:
        file_type = file_types[file_ids.index(file_id)]
        media_group.add(type=file_type, media=file_id)
    return media_group.build()


@dataclass
class DataHandle:
    """Handles merge command."""
    cluster_donors: list[str] = None
    cluster_targets: list[str] = None
    black_text: str = None
    set_text: str = None

    def __init__(self, text: str):
        replaces = ['d', 't', 'del', 'set']

        text = text.replace('/merge ', ' ')
        text = text.replace('/edit_text ', ' ')
        text = text.split(' --')[1:]

        for i in text:
            temp = replaces.index(i.split()[0])
            if temp < 2:
                i = i.split()[1:]
                res = [j.replace(',', '') for j in i]

                if temp == 0:
                    self.cluster_donors = res
                elif temp == 1:
                    self.cluster_targets = res

            elif temp == 2:
                self.black_text = i.replace('del', '', 1)
            elif temp == 3:
                self.set_text = i.replace('set', '', 1)


@dp.message(Command('chat_id'), F.reply)
async def chat_id(message: Message):
    logger.info('Chat info message appeared!')
    await message.answer(str(message.reply_to_message.forward_from_chat.id))


@dp.message(Command('cluster_info'))
async def chat_id(message: Message):
    """/cluster_info <donor>"""
    logger.info('Message cluster_info appeared!')
    donor = message.text.split()[-1]
    base.get_cluster(base.get_cluster_id(donor))


@dp.message(F.chat.id.in_(donors), F.photo)
async def copy_to_targets(message: AlbumMessage):
    """copies message from donor to targets"""
    logger.info('Message to copy appeared!')

    text = message.caption or message.text
    cluster_id = base.get_cluster_id(message.chat.id)
    cluster = base.get_cluster(cluster_id=cluster_id)
    caption = text.replace(cluster[0][3].lstrip(), cluster[0][4].lstrip())

    attachments = []
    media_group = MediaGroupBuilder(caption=caption)
    for m in message:
        for media in {'photo', 'video', 'audio', 'document'}:
            attachment = getattr(m, media, None)
            if attachment:
                attachments.append({'type': media, 'file_id': attachment[-1].file_id})
    for attachment in attachments:
        media_group.add(type=attachment['type'], media=attachment['file_id'])

    for cluster_ in cluster:
        await bot.send_media_group(chat_id=cluster_[2], media=media_group.build())


@dp.message(Command('change_text'), F.chat.id == config["TECHNICAL"])
async def change_text(message: Message):
    """/change_text --d <donor> --del <text_to_del> --set <text_to_set>"""
    data = DataHandle(message.text)
    cluster_id = base.get_cluster_id(data.cluster_donors[0])
    response = base.edit_text(cluster_id=cluster_id,
                              new_text_to_set=data.set_text,
                              new_text_to_del=data.black_text)
    logger.info(response)


@dp.message(Command('merge'), F.chat.id == config["TECHNICAL"])
async def merge(message: Message):
    """/merge --d <donors> --t <targets> --del <text_to_del> --set <texts_to_set>"""
    logger.info('Merge command handled')
    data = DataHandle(message.text)
    max_cluster_id = base.get_max_id()
    print(f'donors: {data.cluster_donors}, targets = {data.cluster_targets},'
          f' text_to_delete = {data.black_text}, text_to_set = {data.set_text}')
    response = base.create_cluster(cluster_id=max_cluster_id+1,
                                   targets=data.cluster_targets,
                                   donors=data.cluster_donors,
                                   text_to_delete=data.black_text,
                                   text_to_set=data.set_text)
    logger.info(response)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    logger.info('Started')
    await dp.start_polling(bot)


if __name__ == "__main__":
    LockAlbumMiddleware(router=dp)
    asyncio.run(main())
