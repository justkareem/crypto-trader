from pyrogram import Client
from pyrogram.handlers import MessageHandler
from open_ai import OpenAi
from bybit import Bybit
from send_email import send_email
from config import telegram_api_id, telegram_api_hash

api_id = telegram_api_id
api_hash = telegram_api_hash
channel_id = -1001920251437


async def hello(client, message):
    if message.chat.id == channel_id:
        print(message)  # Process the message for the specific channel
        if message.text or message.caption:
            if message.caption:
                text = message.caption
            else:
                text = message.text
            if "Future trade signal!".lower() in text.lower():
                process(text)
            elif (("short" or "long") and "tp" and "sl" and "entry") in text.lower():
                process(text)
            elif "warning" in text.lower():
                send_email(text, category="Warning")


def process(text):
    ai = OpenAi(text)
    trade = ai.format_trade()
    exchange = Bybit()
    trader = exchange.place_trade(trade)
    if trader is None:
        return None
    send_email(trader, category="New trade")


app = Client("my_account", api_id, api_hash)

app.add_handler(MessageHandler(hello))

app.run()
