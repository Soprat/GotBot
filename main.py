import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    TelegramObject,
    Message,
)
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_album.lock_middleware import LockAlbumMiddleware
from aiogram_album import AlbumMessage

from database import Database

DEFAULT_DELAY = 0.6
storage = MemoryStorage()
bot_token: str = '6739572759:AAHQepgsUc9wDP-uYGwUMDtScs-GNR26x7M'
dp = Dispatcher()
router = Router(name=__name__)
base = Database()

donors: list[int] = []
technical: int = 
targets: list[int] = []

bot = Bot(bot_token, parse_mode="HTML")


def create_media_group(caption,  file_types: list[str], file_ids) -> list[InputMediaAudio
                                                                          | InputMediaPhoto
                                                                          | InputMediaVideo
                                                                          | InputMediaDocument]:
    media_group = MediaGroupBuilder(caption=caption)
    for file_id in file_ids:
        match file_types[file_ids.index(file_id)-1]:
            case 'photo':
                media_group.add(type='photo', media=file_id)
            case 'video':
                media_group.add(type='video', media=file_id)
            case 'audio':
                media_group.add(type='audio', media=file_id)
            case 'document':
                media_group.add(type='document', media=file_id)
    return media_group.build()


@dp.message(F.media_group_id & F.chat.id.in_(donors))
async def copy_message_to_tech(message: AlbumMessage):
    """This handler will receive a complete album of any type
    and copy from donors to tech"""
    file_ids = []
    file_formats = []
    for m in message:
        content_type = [m.content_type.value][0]
        file_ids.append(str(m.photo[0].file_id))
        file_formats.append(content_type)

    response = base.send(caption=message.caption,
                         file_ids=file_ids,
                         file_formats=file_formats)
    print(response)
    await message.reply(text=str(response))
    await message.copy_to(technical)


@dp.message(Command("send"),
            F.reply_to_message &
            F.reply_to_message.media_group_id)
async def send_message_to_targets(message: AlbumMessage):
    """from tech to targets"""
    await message.answer('sending')
    data = base.get(caption=f'{message.reply_to_message.caption}')
    index = []
    for i in ['photo', 'video', 'audio', 'document']:
        if i in data:
            index.append(data.index(i))
    first_type = min(index)
    file_types = data[first_type:first_type+first_type-1]

    media_group = create_media_group(caption=data[0], file_types=file_types, file_ids=data[1:first_type])

    for channel in targets:
        try:
            await bot.send_media_group(chat_id=channel, media=media_group)
        except Exception as e:
            print(e)


@router.message(Command('info'))
async def get_message_info(message):
    """get info about message on which replied /info"""
    await message.reply_message.answer(message)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    print("Started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    LockAlbumMiddleware(router=dp)
    asyncio.run(main())
