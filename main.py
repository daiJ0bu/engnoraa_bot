import os
import logging
import random
from flask import Flask, request
import requests

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Config
TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not TOKEN:
    logger.error("❌ TELEGRAM_TOKEN not found!")
    exit(1)

if not WEBHOOK_URL:
    logger.error("❌ WEBHOOK_URL not found!")
    exit(1)

API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# 📚 Irregular Verbs Database
IRREGULAR_VERBS = [
    {"base": "be", "past": "was/were", "pp": "been", "uz": "bo'lmoq"},
    {"base": "have", "past": "had", "pp": "had", "uz": "ega bo'lmoq"},
    {"base": "do", "past": "did", "pp": "done", "uz": "qilmoq"},
    {"base": "say", "past": "said", "pp": "said", "uz": "aytmoq"},
    {"base": "go", "past": "went", "pp": "gone", "uz": "bormoq"},
    {"base": "get", "past": "got", "pp": "got/gotten", "uz": "olmoq"},
    {"base": "make", "past": "made", "pp": "made", "uz": "yasamoq"},
    {"base": "know", "past": "knew", "pp": "known", "uz": "bilmoq"},
    {"base": "think", "past": "thought", "pp": "thought", "uz": "o'ylamoq"},
    {"base": "take", "past": "took", "pp": "taken", "uz": "olmoq"},
    {"base": "see", "past": "saw", "pp": "seen", "uz": "ko'rmoq"},
    {"base": "come", "past": "came", "pp": "come", "uz": "kelmoq"},
    {"base": "give", "past": "gave", "pp": "given", "uz": "bermoq"},
    {"base": "find", "past": "found", "pp": "found", "uz": "topmoq"},
    {"base": "tell", "past": "told", "pp": "told", "uz": "aytmoq"},
    {"base": "become", "past": "became", "pp": "become", "uz": "bo'lmoq"},
    {"base": "leave", "past": "left", "pp": "left", "uz": "tark etmoq"},
    {"base": "feel", "past": "felt", "pp": "felt", "uz": "his qilmoq"},
    {"base": "bring", "past": "brought", "pp": "brought", "uz": "olib kelmoq"},
    {"base": "begin", "past": "began", "pp": "begun", "uz": "boshlamoq"},
    {"base": "keep", "past": "kept", "pp": "kept", "uz": "saqlash"},
    {"base": "hold", "past": "held", "pp": "held", "uz": "ushlamoq"},
    {"base": "write", "past": "wrote", "pp": "written", "uz": "yozmoq"},
    {"base": "stand", "past": "stood", "pp": "stood", "uz": "turmoq"},
    {"base": "hear", "past": "heard", "pp": "heard", "uz": "eshitmoq"},
    {"base": "let", "past": "let", "pp": "let", "uz": "ruxsat bermoq"},
    {"base": "mean", "past": "meant", "pp": "meant", "uz": "anglatmoq"},
    {"base": "set", "past": "set", "pp": "set", "uz": "o'rnatmoq"},
    {"base": "meet", "past": "met", "pp": "met", "uz": "uchrashmoq"},
    {"base": "run", "past": "ran", "pp": "run", "uz": "yugurmoq"},
]

# ⏰ Tenses
TENSES = {
    "Present Simple": {
        "formula": "V1 / V1+s",
        "example": "I work every day.\nHe works here.",
        "uz": "Hozirgi oddiy zamon"
    },
    "Present Continuous": {
        "formula": "am/is/are + V+ing",
        "example": "I am working now.\nShe is studying.",
        "uz": "Hozirgi davomli zamon"
    },
    "Present Perfect": {
        "formula": "have/has + V3",
        "example": "I have finished my work.\nHe has left.",
        "uz": "Hozirgi tugallangan zamon"
    },
    "Past Simple": {
        "formula": "V2",
        "example": "I worked yesterday.\nShe came home.",
        "uz": "O'tgan oddiy zamon"
    },
    "Past Continuous": {
        "formula": "was/were + V+ing",
        "example": "I was working at 5pm.",
        "uz": "O'tgan davomli zamon"
    },
    "Past Perfect": {
        "formula": "had + V3",
        "example": "I had finished before he came.",
        "uz": "O'tgan tugallangan zamon"
    },
    "Future Simple": {
        "formula": "will + V1",
        "example": "I will work tomorrow.\nShe will come.",
        "uz": "Kelasi oddiy zamon"
    },
    "Future Continuous": {
        "formula": "will be + V+ing",
        "example": "I will be working at 5pm tomorrow.",
        "uz": "Kelasi davomli zamon"
    },
    "Future Perfect": {
        "formula": "will have + V3",
        "example": "I will have finished by 5pm.",
        "uz": "Kelasi tugallangan zamon"
    },
}

# 💬 Daily Phrases
DAILY_PHRASES = [
    {"en": "Good morning!", "uz": "Xayrli tong!"},
    {"en": "How are you?", "uz": "Qalaysiz?"},
    {"en": "Thank you", "uz": "Rahmat"},
    {"en": "You're welcome", "uz": "Arzimaydi"},
    {"en": "Excuse me", "uz": "Kechirasiz"},
    {"en": "I don't understand", "uz": "Men tushunmadim"},
    {"en": "Can you help me?", "uz": "Yordam bera olasizmi?"},
    {"en": "See you later", "uz": "Ko'rishguncha"},
    {"en": "Nice to meet you", "uz": "Tanishganimdan xursandman"},
    {"en": "Have a nice day!", "uz": "Kuningiz xayrli o'tsin!"},
]

def send_message(chat_id, text, reply_markup=None):
    """Send message to Telegram"""
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    
    try:
        response = requests.post(f"{API_URL}/sendMessage", json=data, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return None

def get_main_menu():
    """Main menu keyboard"""
    return {
        "inline_keyboard": [
            [
                {"text": "🌐 Open Web App", "web_app": {"url": "https://engnoraa.vercel.app"}}
            ],
            [
                {"text": "📚 Random Verb", "callback_data": "random_verb"},
                {"text": "🎮 Verb Quiz", "callback_data": "verb_quiz"}
            ],
            [
                {"text": "⏰ Random Tense", "callback_data": "random_tense"},
                {"text": "📖 All Tenses", "callback_data": "all_tenses"}
            ],
            [
                {"text": "💬 Daily Phrase", "callback_data": "daily_phrase"},
                {"text": "❓ Help", "callback_data": "help"}
            ]
        ]
    }

@app.route("/")
def home():
    return "✅ Engnoraa Interactive Bot v2.0 is running!", 200

@app.route("/health")
def health():
    return {"status": "ok", "version": "2.0"}, 200

@app.route("/setup")
def setup():
    """Setup webhook"""
    webhook_url = f"{WEBHOOK_URL}/webhook"
    
    # Delete old webhook
    requests.post(f"{API_URL}/deleteWebhook", timeout=10)
    logger.info("🗑️ Old webhook deleted")
    
    # Set new webhook
    response = requests.post(
        f"{API_URL}/setWebhook",
        json={"url": webhook_url},
        timeout=10
    )
    
    result = response.json()
    logger.info(f"✅ Webhook setup: {result}")
    return result, 200

@app.route("/info")
def info():
    """Webhook info"""
    response = requests.get(f"{API_URL}/getWebhookInfo", timeout=10)
    return response.json(), 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle webhook updates"""
    try:
        update = request.get_json()
        
        # Handle messages
        if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            user = message.get("from", {})
            
            logger.info(f"Message from {user.get('id')}: {text}")
            
            if text == "/start":
                send_message(
                    chat_id,
                    "👋 Welcome to <b>Engnoraa English</b>!\n\n"
                    "🎯 Learn English interactively:\n"
                    "📚 30+ Irregular Verbs\n"
                    "⏰ 9 Essential Tenses\n"
                    "🎮 Interactive Quizzes\n"
                    "💬 Daily Useful Phrases\n\n"
                    "Choose an option below or open the Web App! 🚀",
                    get_main_menu()
                )
                
            elif text == "/help":
                send_message(
                    chat_id,
                    "❓ <b>How to use Engnoraa Bot</b>\n\n"
                    "📚 <b>Random Verb</b> - Learn irregular verbs\n"
                    "🎮 <b>Verb Quiz</b> - Test your knowledge\n"
                    "⏰ <b>Random Tense</b> - Study tenses with examples\n"
                    "📖 <b>All Tenses</b> - Quick reference\n"
                    "💬 <b>Daily Phrase</b> - Useful expressions\n"
                    "🌐 <b>Web App</b> - Full interactive experience\n\n"
                    "💡 Tip: Use the Web App for the best experience!",
                    get_main_menu()
                )
            else:
                send_message(
                    chat_id,
                    "ℹ️ Use /start to see the menu",
                    get_main_menu()
                )
        
        # Handle callback queries (button presses)
        elif "callback_query" in update:
            callback = update["callback_query"]
            chat_id = callback["message"]["chat"]["id"]
            data = callback["data"]
            
            logger.info(f"Callback from {chat_id}: {data}")
            
            if data == "random_verb":
                verb = random.choice(IRREGULAR_VERBS)
                text = (
                    f"📚 <b>Irregular Verb</b>\n\n"
                    f"🔹 <b>Base Form:</b> {verb['base']}\n"
                    f"🔹 <b>Past Simple:</b> {verb['past']}\n"
                    f"🔹 <b>Past Participle:</b> {verb['pp']}\n"
                    f"🇺🇿 <b>Tarjima:</b> {verb['uz']}\n\n"
                    f"💡 <i>I {verb['base']} / I {verb['past']} / I have {verb['pp']}</i>"
                )
                send_message(chat_id, text, get_main_menu())
            
            elif data == "verb_quiz":
                verb = random.choice(IRREGULAR_VERBS)
                # Create 3 options (1 correct + 2 wrong)
                options = [verb["past"]]
                while len(options) < 3:
                    wrong = random.choice(IRREGULAR_VERBS)["past"]
                    if wrong not in options:
                        options.append(wrong)
                random.shuffle(options)
                
                quiz_markup = {
                    "inline_keyboard": [
                        [{"text": opt, "callback_data": f"quiz_{verb['base']}_{opt}"}] 
                        for opt in options
                    ] + [[{"text": "🔙 Back to Menu", "callback_data": "back"}]]
                }
                
                send_message(
                    chat_id,
                    f"🎮 <b>Verb Quiz</b>\n\n"
                    f"What is the <b>past form</b> of:\n\n"
                    f"<code>{verb['base']}</code> ({verb['uz']})?",
                    quiz_markup
                )
            
            elif data.startswith("quiz_"):
                parts = data.split("_", 2)
                base = parts[1]
                answer = parts[2]
                correct_verb = next((v for v in IRREGULAR_VERBS if v["base"] == base), None)
                
                if correct_verb and answer == correct_verb["past"]:
                    text = (
                        f"✅ <b>Correct!</b> 🎉\n\n"
                        f"{base} → {correct_verb['past']} → {correct_verb['pp']}\n\n"
                        f"Great job! 👏"
                    )
                else:
                    text = (
                        f"❌ <b>Oops!</b>\n\n"
                        f"Correct answer:\n"
                        f"{base} → <b>{correct_verb['past']}</b> → {correct_verb['pp']}\n\n"
                        f"Keep practicing! 💪"
                    )
                
                send_message(chat_id, text, get_main_menu())
            
            elif data == "random_tense":
                tense_name = random.choice(list(TENSES.keys()))
                tense = TENSES[tense_name]
                text = (
                    f"⏰ <b>{tense_name}</b>\n"
                    f"🇺🇿 {tense['uz']}\n\n"
                    f"📝 <b>Formula:</b>\n<code>{tense['formula']}</code>\n\n"
                    f"💡 <b>Examples:</b>\n{tense['example']}"
                )
                send_message(chat_id, text, get_main_menu())
            
            elif data == "all_tenses":
                text = "📖 <b>All English Tenses</b>\n\n"
                for i, (name, info) in enumerate(TENSES.items(), 1):
                    text += f"{i}. <b>{name}</b>\n   {info['formula']}\n\n"
                text += "💡 Click 'Random Tense' to see examples!"
                send_message(chat_id, text, get_main_menu())
            
            elif data == "daily_phrase":
                phrase = random.choice(DAILY_PHRASES)
                text = (
                    f"💬 <b>Daily Phrase</b>\n\n"
                    f"🇬🇧 {phrase['en']}\n"
                    f"🇺🇿 {phrase['uz']}\n\n"
                    f"💡 Try using this phrase today!"
                )
                send_message(chat_id, text, get_main_menu())
            
            elif data == "help":
                send_message(
                    chat_id,
                    "❓ <b>Help</b>\n\n"
                    "Use the buttons below to learn English!\n"
                    "For the full experience, open the Web App 🌐",
                    get_main_menu()
                )
            
            elif data == "back":
                send_message(chat_id, "🏠 <b>Main Menu</b>", get_main_menu())
            
            # Answer callback query
            requests.post(
                f"{API_URL}/answerCallbackQuery",
                json={"callback_query_id": callback["id"]},
                timeout=5
            )
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}", exc_info=True)
        return "Error", 500

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    logger.info(f"🚀 Starting Engnoraa Bot on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)