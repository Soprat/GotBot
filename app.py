import asyncio
from pyrogram import Client, filters



class App():
    '''main class'''
    def __init__(self):
        from dotenv import load_dotenv, find_dotenv
        from os import environ

        load_dotenv(find_dotenv())

        API_ID: int = environ.get('API_ID')
        API_HASH: str = environ.get('API_HASH')
        BOT_TOKEN: str = environ.get('BOT_TOKEN')

        self.app = Client("app",
                          api_id=API_ID,
                          api_hash=API_HASH,
                          bot_token=BOT_TOKEN)

    def creating(self):
        '''Creating of app'''
        return self.app

    async def join(self, chat_ids: list):
        '''Allows bot to join to chats, set in chat_ids'''
        App()
        for chat_id in map(chat_ids):
            try:
                await self.app.join_chat(chat_id)
            except Exception:
                chat_ids.pop(chat_id)

        return f'Sucessfully joined to {len(chat_ids)} channels'
