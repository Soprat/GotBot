'''module providing asynchronous work of code'''
import asyncio
from pyrogram import filters
from data import DB_action, Ids
from app import App

db = DB_action()
ids = Ids()
app = App().creating()


@app.on_message(filters.channel &
                filters.chat(ids.donors))
async def copy_message_to_tech(message):
    '''Copies message from donor's channels to tech'''
    await app.copy_message(
        chat_id=ids.tech,
        from_chat_id=message.chat.id,
        message_id=message.id)


@app.on_message(filters=filters.command(["send"]) &
                filters.chat(ids.tech) &
                filters.reply)
async def send(message):
    '''Sends messages to targets from tech channel'''
    for chat_id in ids.targets:
        try:
            await app.copy_message(
                chat_id=chat_id,
                from_chat_id=ids.tech,
                message_id=message.reply_to_message.id)
        except Exception as e:
            await app.send_message(
                chat_id=message.reply_to_message.chat.id,
                text=f'Error sending message to {chat_id}: {e}')


@app.on_message(filters=filters.command(['add_donors']) &
                filters.chat(ids.tech) &
                filters.reply)
async def add_donors(message):
    ''' At command 'add_targets' with replying to message,
        bot will add channel's id's in replied  to 'Targets' in database'''
    await app.send_message(
        chat_id=message.reply_to_message.chat.id,
        text=db.send("Donors", message.reply_to_message.text))

@app.on_message(filters=filters.command(['add_targets']) &
                filters.chat(ids.tech) &
                filters.reply)
async def add_targets(message):
    """At command 'add_targets' with replying to message,
        bot will add channel's id's in replied  to 'Targets' in database"""
    await app.send_message(
        chat_id=message.reply_to_message.chat.id, 
        text=db.send("Targets", message.reply_to_message.text))


@app.on_message(filters=filters.command(['join']) &
                filters.chat(ids.tech) &
                filters.reply)
async def join_channels(message):
    """At command 'join' with replying to message, bot will
        join to channels, wroten in this message"""
    await app.send_message(
        chat_id=message.reply_to_message.chat.id,
        text=App.join(chat_ids=message.text.replace(" ", "").split(",")))

asyncio.run(app.run())
