import os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Logging sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # https://your-app.onrender.com

if not TOKEN:
    raise Exception("❌ TELEGRAM_TOKEN env variable topilmadi!")
if not WEBHOOK_URL:
    raise Exception("❌ WEBHOOK_URL env variable topilmadi!")

# Bot va Dispatcher
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Flask app
app = Flask(__name__)

# /start komandasi
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

# Boshqa xabarlar uchun (ixtiyoriy)
@dp.message(F.text)
async def echo_handler(message: types.Message):
    await message.answer(
        "ℹ️ Use /start to open the app"
    )

# Health check endpoint
@app.route("/", methods=["GET"])
def home():
    return "✅ Engnoraa bot is running!", 200

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        update_data = request.get_json()
        update = types.Update.model_validate(update_data)
        
        # Async funksiyani sync rejimda ishga tushirish
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        loop.run_until_complete(dp.feed_update(bot, update))
        return "OK", 200
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return "Error", 500

# Webhook o'rnatish
async def on_startup():
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    logger.info(f"✅ Webhook set: {webhook_url}")

# Webhook o'chirish
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("🛑 Webhook deleted")

if __name__ == "__main__":
    import asyncio
    
    # Webhook o'rnatish
    asyncio.run(on_startup())
    
    # Flask serverni ishga tushirish
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)