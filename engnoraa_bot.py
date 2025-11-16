# import os
# import asyncio
# import logging
# from threading import Thread
# from flask import Flask
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.enums import ParseMode
# from aiogram.client.default import DefaultBotProperties
# from aiogram.filters import CommandStart

# # Logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Token (Render'da environment variable'dan oqiladi)
# TOKEN = os.environ.get("TELEGRAM_TOKEN", "8175905001:AAEiUDItp344S3MmFGQIzInVO_nnPwhDSjs")

# # Bot
# bot = Bot(
#     token=TOKEN,
#     default=DefaultBotProperties(parse_mode=ParseMode.HTML)
# )
# dp = Dispatcher()

# # Flask (Render uxlamasligi uchun)
# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "✅ Engnoraa bot is running!"

# @app.route("/health")
# def health():
#     return {"status": "ok"}

# # /start komandasi
# @dp.message(CommandStart())
# async def start_command(message: types.Message):
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text="🌐 Open Engnoraa",
#                     web_app=WebAppInfo(url="https://engnoraa.vercel.app")
#                 )
#             ]
#         ]
#     )
    
#     await message.answer(
#         "👋 Welcome to <b>Engnoraa English</b>!\n"
#         "Learn, play and test your English 🌟",
#         reply_markup=keyboard
#     )
    
#     logger.info(f"✅ User {message.from_user.id} started bot")

# # Bot ishga tushirish
# async def start_bot():
#     try:
#         # Webhook o'chirish (agar mavjud bo'lsa)
#         await bot.delete_webhook(drop_pending_updates=True)
#         logger.info("🗑️ Webhook deleted")
        
#         logger.info("🤖 Bot polling started!")
#         await dp.start_polling(bot)
#     except Exception as e:
#         logger.error(f"❌ Bot error: {e}")

# def run_bot():
#     asyncio.run(start_bot())

# if __name__ == "__main__":
#     # Bot'ni background thread'da ishga tushirish
#     bot_thread = Thread(target=run_bot, daemon=True)
#     bot_thread.start()
#     logger.info("🚀 Bot thread started")
    
#     # Flask server
#     PORT = int(os.environ.get("PORT", 5000))
#     logger.info(f"🌐 Flask running on port {PORT}")
#     app.run(host="0.0.0.0", port=PORT)