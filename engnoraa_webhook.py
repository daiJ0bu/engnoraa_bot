import os
import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_TOKEN env variable TOPILMADI!")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
app = Flask(__name__)

# --- Home test route ---
@app.route("/", methods=["GET"])
def home():
    return "Engnoraa bot is running!"

# --- Handler ---
@dp.message()
async def start(message: types.Message):
    if message.text == "/start":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🌐 Open Engnoraa",
                        web_app=WebAppInfo(url="https://engnoraa.vercel.app")
                    )
                ]
            ]
        )
        await message.answer(
            "👋 Welcome to <b>Engnoraa English</b>!\nLearn, play and test your English 🌟",
            reply_markup=keyboard
        )

# --- Webhook route ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = types.Update.de_json(request.get_json())
    asyncio.run(dp.process_update(update))
    return "OK"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    print(f"🌐 Running on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
