from flask import Flask, request
from aiogram import Bot, Dispatcher, types
import asyncio
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")  # ENV variable nomi
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask(__name__)

@dp.message()
async def start(message: types.Message):
    if message.text == "/start":
        await message.answer("🤖 Engnoraa bot ishlayapti!")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_str)
    asyncio.run(dp.process_update(update))
    return "OK"
