import os
import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_TOKEN env variable TOPILMADI!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Engnoraa bot is running!"

@dp.message()
async def start(message: types.Message):
    if message.text == "/start":
        await message.answer("🤖 Engnoraa webhook bot ishlayapti!")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = types.Update.de_json(request.get_json())
    asyncio.run(dp.process_update(update))
    return "OK"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
