import json
import re
import time
import os
import sys

from telethon import TelegramClient, events, Button
from telethon.tl.types import PeerChannel
from Database import Db as db
from Helper import Helper
from datetime import datetime

""" config.json file ichidagi sozlamarni chaqirish massiv holatida """
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'config.json'), 'r',
          encoding='utf-8') as file:
    config = json.load(file)

""" Bot sessiya saqlaydigan faylni joyini korsatish """
session_bot = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'bot')

""" Telegram Clientga ulanish """
bot = TelegramClient(session_bot, config['api_id'], config['api_hash']).start(bot_token=config['token'])

""" message.json file ichidagi so'zlarni chaqirish massiv holatida """
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'messages.json'), 'r',
          encoding='utf-8') as file:
    message = json.load(file)

status = {'status': ""}


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    status['status'] = "start"

    fullname = "{} {}".format(
        event.sender.first_name,
        event.sender.last_name
    )

    if not Helper.isChannel(event.message):
        return

    db.insertUser({
        'user_id': event.sender.id,
        'fullname': fullname.replace('None', ''),
        'created_date': datetime.today()
    })

    if db.user_info(event.sender.id)['block']:
        await event.reply(message['block'].replace('{user}', fullname.replace('None', '')), parse_mode="HTML")
        raise events.StopPropagation

    await event.reply(message['welcome'], buttons=Button.text('💻 Buyurtma berish', resize=True), parse_mode="HTML")
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="💻 Buyurtma berish"))
async def click_order(event):
    fullname = "{} {}".format(
        event.sender.first_name,
        event.sender.last_name
    )

    if db.user_info(event.sender.id)['block']:
        await event.reply(message['block'].replace('{user}', fullname.replace('None', '')), parse_mode="HTML")
        raise events.StopPropagation

    status['status'] = "order"

    await event.reply(
        message['click_order'].replace('{user}', fullname.replace('None', '')),
        buttons=Button.text('💻 Buyurtma berish', resize=True),
        parse_mode="HTML")
    raise events.StopPropagation


@bot.on(events.NewMessage(func=lambda e:
e.message.message != "/start" and
e.message.message != "Buyurtma berish" and
e.message.message != r"/block=*.(?i)"))
async def order(event):
    fullname = "{} {}".format(
        event.sender.first_name,
        event.sender.last_name
    )

    if not Helper.isChannel(event.message):
        return

    if status['status'] != "order":
        await event.reply(message['welcome'], parse_mode="HTML")
        raise events.StopPropagation

    if db.user_info(event.sender.id)['block']:
        await event.reply(message['block'].replace('{user}', fullname.replace('None', '')), parse_mode="HTML")
        raise events.StopPropagation

    order = db.insertOrder({
        'user_id': event.sender.id,
        'order_text': event.message.message,
        'created_date': str(datetime.today())
    })

    channel = await bot.get_entity(PeerChannel(config['channel']))

    await bot.send_message(
        channel,
        "👨‍💻 Buyurtma: <b>{}</b>\n👨‍💻 Buyurtmachi: #{} | <a href='tg://user?id={}'>{}</a>\n\n✅ Matn:\n\n{}‍".format(
            order['id'], event.sender.id, event.sender.id, fullname.replace('None', ''), event.message.message
        ),
        parse_mode='HTML'
    )
    status['status'] = "order_success"
    await event.reply(message['order'].replace('{user}', fullname.replace('None', '')), parse_mode="HTML")
    raise events.StopPropagation


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
