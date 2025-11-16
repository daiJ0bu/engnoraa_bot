# import os
# import logging
# from flask import Flask, request
# import requests

# # Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Config
# TOKEN = os.environ.get("TELEGRAM_TOKEN", "8175905001:AAEiUDItp344S3MmFGQIzInVO_nnPwhDSjs")
# WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://engnoraa-bot.onrender.com")

# API_URL = f"https://api.telegram.org/bot{TOKEN}"

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "✅ Engnoraa bot is running!", 200

# @app.route("/setup")
# def setup():
#     """Webhook o'rnatish"""
#     webhook_url = f"{WEBHOOK_URL}/webhook"
    
#     # Eski webhook o'chirish
#     requests.post(f"{API_URL}/deleteWebhook")
    
#     # Yangi webhook
#     response = requests.post(
#         f"{API_URL}/setWebhook",
#         json={"url": webhook_url}
#     )
    
#     result = response.json()
#     logger.info(f"Webhook setup: {result}")
#     return result, 200

# @app.route("/info")
# def info():
#     """Webhook info"""
#     response = requests.get(f"{API_URL}/getWebhookInfo")
#     return response.json(), 200

# @app.route("/webhook", methods=["POST"])
# def webhook():
#     """Telegram'dan xabar qabul qilish"""
#     try:
#         update = request.get_json()
        
#         # /start komandasi
#         if "message" in update and "text" in update["message"]:
#             chat_id = update["message"]["chat"]["id"]
#             text = update["message"]["text"]
            
#             if text == "/start":
#                 # Web App button
#                 reply_markup = {
#                     "inline_keyboard": [[
#                         {
#                             "text": "🌐 Open Engnoraa",
#                             "web_app": {"url": "https://engnoraa.vercel.app"}
#                         }
#                     ]]
#                 }
                
#                 # Javob yuborish
#                 requests.post(
#                     f"{API_URL}/sendMessage",
#                     json={
#                         "chat_id": chat_id,
#                         "text": "👋 Welcome to <b>Engnoraa English</b>!\nLearn, play and test your English 🌟",
#                         "parse_mode": "HTML",
#                         "reply_markup": reply_markup
#                     }
#                 )
                
#                 logger.info(f"✅ User {chat_id} started bot")
        
#         return "OK", 200
        
#     except Exception as e:
#         logger.error(f"❌ Error: {e}")
#         return "Error", 500

# if __name__ == "__main__":
#     PORT = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=PORT)