# import os
# import logging
# from flask import Flask, request, jsonify
# from aiogram import Bot, Dispatcher, types, F
# from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.enums import ParseMode
# from aiogram.client.default import DefaultBotProperties
# from aiogram.filters import CommandStart
# from dotenv import load_dotenv

# # Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# load_dotenv()

# TOKEN = os.environ.get("TELEGRAM_TOKEN")
# WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# if not TOKEN:
#     raise Exception("❌ TELEGRAM_TOKEN topilmadi!")
# if not WEBHOOK_URL:
#     raise Exception("❌ WEBHOOK_URL topilmadi!")

# # Bot
# bot = Bot(
#     token=TOKEN,
#     default=DefaultBotProperties(parse_mode=ParseMode.HTML)
# )
# dp = Dispatcher()

# # Flask
# app = Flask(__name__)

# # ✅ /start komandasi
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
#     logger.info(f"User {message.from_user.id} started the bot")

# # ✅ Boshqa xabarlar
# @dp.message(F.text)
# async def other_messages(message: types.Message):
#     await message.answer("ℹ️ Use /start to open the app")

# # ✅ Health check
# @app.route("/", methods=["GET"])
# def home():
#     return "✅ Engnoraa bot is running!", 200

# # ✅ Webhook endpoint (SYNC versiya - Render uchun)
# @app.route(f"/{TOKEN}", methods=["POST"])
# def webhook():
#     import asyncio
    
#     try:
#         update_data = request.get_json()
#         if not update_data:
#             logger.error("Empty update received")
#             return "Error: Empty update", 400
        
#         update = types.Update.model_validate(update_data)
#         logger.info(f"Received update: {update.update_id}")
        
#         # Async funksiyani sync rejimda ishga tushirish
#         try:
#             loop = asyncio.get_event_loop()
#         except RuntimeError:
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
        
#         loop.run_until_complete(dp.feed_update(bot, update))
        
#         return "OK", 200
        
#     except Exception as e:
#         logger.error(f"Error processing update: {e}", exc_info=True)
#         return jsonify({"error": str(e)}), 500

# # ✅ Webhook info (debug uchun)
# @app.route("/webhook-info", methods=["GET"])
# def webhook_info():
#     import asyncio
    
#     try:
#         loop = asyncio.get_event_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
    
#     info = loop.run_until_complete(bot.get_webhook_info())
    
#     return jsonify({
#         "url": info.url,
#         "has_custom_certificate": info.has_custom_certificate,
#         "pending_update_count": info.pending_update_count,
#         "last_error_date": info.last_error_date,
#         "last_error_message": info.last_error_message,
#         "max_connections": info.max_connections
#     })

# # ✅ Webhook o'rnatish
# def setup_webhook():
#     import asyncio
    
#     webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    
#     try:
#         loop = asyncio.get_event_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
    
#     try:
#         # Eski webhook o'chirish
#         loop.run_until_complete(bot.delete_webhook(drop_pending_updates=True))
#         logger.info("🗑️ Old webhook deleted")
        
#         # Yangi webhook o'rnatish
#         loop.run_until_complete(bot.set_webhook(webhook_url))
#         logger.info(f"✅ Webhook set: {webhook_url}")
        
#         # Tekshirish
#         info = loop.run_until_complete(bot.get_webhook_info())
#         logger.info(f"📊 Webhook info: {info.url}")
        
#     except Exception as e:
#         logger.error(f"❌ Webhook setup failed: {e}")
#         raise

# if __name__ == "__main__":
#     # Webhook o'rnatish
#     setup_webhook()
    
#     # Flask server
#     PORT = int(os.environ.get("PORT", 5000))
#     logger.info(f"🚀 Starting server on port {PORT}")
#     app.run(host="0.0.0.0", port=PORT)