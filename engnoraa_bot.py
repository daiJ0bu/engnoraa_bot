import os
import asyncio
import logging
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise Exception("❌ TELEGRAM_TOKEN topilmadi!")

# Bot
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Flask (Render uchun kerak - uxlab qolmasligi uchun)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Engnoraa bot is running!", 200

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "bot": "online"}, 200

# ✅ /start komandasi
@dp.message(CommandStart())
async def start_command(message: types.Message):
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
        "👋 Welcome to <b>Engnoraa English</b>!\n"
        "Learn, play and test your English 🌟",
        reply_markup=keyboard
    )
    
    logger.info(f"✅ User {message.from_user.id} started the bot")

# ✅ Boshqa xabarlar
@dp.message(F.text)
async def other_messages(message: types.Message):
    await message.answer("ℹ️ Use /start to open the app")

# ✅ Bot ishga tushirish (alohida thread'da)
async def start_bot():
    try:
        logger.info("🤖 Engnoraa bot started!")
        bot_info = await bot.get_me()
        logger.info(f"Bot: @{bot_info.username}")
        
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")

def run_bot():
    """Bot'ni alohida thread'da ishga tushirish"""
    asyncio.run(start_bot())

if __name__ == "__main__":
    # Bot'ni background'da ishga tushirish
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    logger.info("🚀 Flask server starting...")
    
    # Flask serverni ishga tushirish
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)