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
from aiogram_album.lock_middleware import LockAlbumMiddleware

from database import Database

DEFAULT_DELAY = 0.6
storage = MemoryStorage()
bot_token: str = '6739572759:AAHQepgsUc9wDP-uYGwUMDtScs-GNR26x7M'
dp = Dispatcher()
router = Router(name=__name__)

donors: list[int] = [-4093149059]
technical: int = -1002085744420

bot = Bot(bot_token, parse_mode="HTML")


@dp.message(F.media_group_id)
async def copy_message_to_tech(message: Message):
    """This handler will receive a complete album of any type
    and copy from donors to tech"""
    print(message.caption, message.media_group_id, "\n\n", [m.photo for m in message])
    print([m.photo for m in message][0])
    await message.copy_to(technical)
    return


@dp.message(Command("send"),
            F.reply_to_message,
            F.reply_to_message.media_group_id)
async def send_message_to_targets(message: Message):
    """from tech to targets"""
    targets: list[int] = [-4093149059]
    await message.answer('sending')

    for channel in targets:
        # await message.reply_to_message.copy_to(chat_id=channel)
        try:
            # noinspection PyUnresolvedReferences
            await message.reply_to_message.message_id.forward(chat_id=channel)
        except AttributeError:
            pass
        # await message.copy_to(chat_id=channel)


@router.message(Command('info'))
async def get_message_info(message):
    # await bot.send_media_group(message.chat.id, media=files)
    await message.answer(message)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    print("Started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    LockAlbumMiddleware(router=dp)
    asyncio.run(main())
