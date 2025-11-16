import os
import logging
import random
from flask import Flask, request
import requests

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8175905001:AAEiUDItp344S3MmFGQIzInVO_nnPwhDSjs")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://engnoraa-bot.onrender.com")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# 📚 Irregular Verbs (100 ta eng mashhur)
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
    {"base": "want", "past": "wanted", "pp": "wanted", "uz": "xohlamoq"},
    {"base": "give", "past": "gave", "pp": "given", "uz": "bermoq"},
    {"base": "find", "past": "found", "pp": "found", "uz": "topmoq"},
    {"base": "tell", "past": "told", "pp": "told", "uz": "aytmoq"},
    {"base": "become", "past": "became", "pp": "become", "uz": "bo'lmoq"},
    {"base": "leave", "past": "left", "pp": "left", "uz": "tark etmoq"},
    {"base": "feel", "past": "felt", "pp": "felt", "uz": "his qilmoq"},
    {"base": "bring", "past": "brought", "pp": "brought", "uz": "olib kelmoq"},
]

# 🎮 Tenses (12 ta zamon)
TENSES = {
    "Present Simple": {
        "formula": "V1 / V1+s",
        "example": "I work every day. / He works here.",
        "uz": "Hozirgi oddiy zamon"
    },
    "Present Continuous": {
        "formula": "am/is/are + V+ing",
        "example": "I am working now. / She is studying.",
        "uz": "Hozirgi davomli zamon"
    },
    "Present Perfect": {
        "formula": "have/has + V3",
        "example": "I have finished my work. / He has left.",
        "uz": "Hozirgi tugallangan zamon"
    },
    "Present Perfect Continuous": {
        "formula": "have/has been + V+ing",
        "example": "I have been working for 2 hours.",
        "uz": "Hozirgi tugallangan davomli"
    },
    "Past Simple": {
        "formula": "V2",
        "example": "I worked yesterday. / She came home.",
        "uz": "O'tgan oddiy zamon"
    },
    "Past Continuous": {
        "formula": "was/were + V+ing",
        "example": "I was working at 5pm yesterday.",
        "uz": "O'tgan davomli zamon"
    },
    "Past Perfect": {
        "formula": "had + V3",
        "example": "I had finished before he came.",
        "uz": "O'tgan tugallangan zamon"
    },
    "Past Perfect Continuous": {
        "formula": "had been + V+ing",
        "example": "I had been working for 2 hours when he arrived.",
        "uz": "O'tgan tugallangan davomli"
    },
    "Future Simple": {
        "formula": "will + V1",
        "example": "I will work tomorrow. / She will come.",
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
    "Future Perfect Continuous": {
        "formula": "will have been + V+ing",
        "example": "I will have been working for 2 hours by then.",
        "uz": "Kelasi tugallangan davomli"
    }
}

# 💬 Daily Phrases
DAILY_PHRASES = [
    {"en": "Good morning!", "uz": "Xayrli tong!", "pronunciation": "gud mo:ning"},
    {"en": "How are you?", "uz": "Qalaysiz?", "pronunciation": "hau a: yu"},
    {"en": "Thank you", "uz": "Rahmat", "pronunciation": "θæŋk yu"},
    {"en": "You're welcome", "uz": "Arzimaydi", "pronunciation": "yo: welkəm"},
    {"en": "Excuse me", "uz": "Kechirasiz", "pronunciation": "ikskyu:z mi:"},
    {"en": "I don't understand", "uz": "Men tushunmadim", "pronunciation": "ai dount ʌndəstænd"},
    {"en": "Can you help me?", "uz": "Yordam bera olasizmi?", "pronunciation": "kæn yu help mi:"},
    {"en": "See you later", "uz": "Ko'rishguncha", "pronunciation": "si: yu leitə"},
]

def send_message(chat_id, text, reply_markup=None):
    """Telegram'ga xabar yuborish"""
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    
    requests.post(f"{API_URL}/sendMessage", json=data)

def get_main_menu():
    """Asosiy menyu"""
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
    return "✅ Engnoraa Interactive Bot is running!", 200

@app.route("/setup")
def setup():
    """Webhook o'rnatish"""
    webhook_url = f"{WEBHOOK_URL}/webhook"
    requests.post(f"{API_URL}/deleteWebhook")
    response = requests.post(f"{API_URL}/setWebhook", json={"url": webhook_url})
    return response.json(), 200

@app.route("/info")
def info():
    """Webhook info"""
    response = requests.get(f"{API_URL}/getWebhookInfo")
    return response.json(), 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """Telegram webhook"""
    try:
        update = request.get_json()
        
        # Xabar
        if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            
            if text == "/start":
                send_message(
                    chat_id,
                    "👋 Welcome to <b>Engnoraa English</b>!\n\n"
                    "🎯 Learn English with:\n"
                    "📚 Irregular Verbs\n"
                    "⏰ 12 Tenses\n"
                    "🎮 Interactive Games\n"
                    "💬 Daily Phrases\n\n"
                    "Choose an option below:",
                    get_main_menu()
                )
                
            elif text == "/help":
                send_message(
                    chat_id,
                    "❓ <b>Help</b>\n\n"
                    "📚 <b>Random Verb</b> - Get random irregular verb\n"
                    "🎮 <b>Verb Quiz</b> - Test your knowledge\n"
                    "⏰ <b>Random Tense</b> - Learn random tense\n"
                    "📖 <b>All Tenses</b> - See all 12 tenses\n"
                    "💬 <b>Daily Phrase</b> - Learn useful phrases\n"
                    "🌐 <b>Web App</b> - Full interactive experience",
                    get_main_menu()
                )
        
        # Callback (tugmalar)
        elif "callback_query" in update:
            callback = update["callback_query"]
            chat_id = callback["message"]["chat"]["id"]
            data = callback["data"]
            
            if data == "random_verb":
                verb = random.choice(IRREGULAR_VERBS)
                text = (
                    f"📚 <b>Irregular Verb</b>\n\n"
                    f"🔹 <b>Base:</b> {verb['base']}\n"
                    f"🔹 <b>Past:</b> {verb['past']}\n"
                    f"🔹 <b>Past Participle:</b> {verb['pp']}\n"
                    f"🇺🇿 <b>Ma'nosi:</b> {verb['uz']}\n\n"
                    f"💡 <i>Example: I {verb['base']} / I {verb['past']} / I have {verb['pp']}</i>"
                )
                send_message(chat_id, text, get_main_menu())
            
            elif data == "verb_quiz":
                verb = random.choice(IRREGULAR_VERBS)
                # Quiz uchun 3 ta variant (1 to'g'ri + 2 noto'g'ri)
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
                    ] + [[{"text": "🔙 Back", "callback_data": "back"}]]
                }
                
                send_message(
                    chat_id,
                    f"🎮 <b>Verb Quiz</b>\n\n"
                    f"What is the past form of '<b>{verb['base']}</b>'?",
                    quiz_markup
                )
            
            elif data.startswith("quiz_"):
                parts = data.split("_")
                base = parts[1]
                answer = parts[2]
                correct_verb = next((v for v in IRREGULAR_VERBS if v["base"] == base), None)
                
                if correct_verb and answer == correct_verb["past"]:
                    text = f"✅ <b>Correct!</b>\n\n{base} → {correct_verb['past']} → {correct_verb['pp']}"
                else:
                    text = f"❌ <b>Wrong!</b>\n\nCorrect: {base} → {correct_verb['past']} → {correct_verb['pp']}"
                
                send_message(chat_id, text, get_main_menu())
            
            elif data == "random_tense":
                tense_name = random.choice(list(TENSES.keys()))
                tense = TENSES[tense_name]
                text = (
                    f"⏰ <b>{tense_name}</b>\n"
                    f"🇺🇿 {tense['uz']}\n\n"
                    f"📝 <b>Formula:</b> {tense['formula']}\n\n"
                    f"💡 <b>Example:</b>\n{tense['example']}"
                )
                send_message(chat_id, text, get_main_menu())
            
            elif data == "all_tenses":
                text = "📖 <b>All 12 Tenses</b>\n\n"
                for name, info in TENSES.items():
                    text += f"• <b>{name}</b>: {info['formula']}\n"
                text += "\n💡 Use /start to explore each tense!"
                send_message(chat_id, text, get_main_menu())
            
            elif data == "daily_phrase":
                phrase = random.choice(DAILY_PHRASES)
                text = (
                    f"💬 <b>Daily Phrase</b>\n\n"
                    f"🇬🇧 {phrase['en']}\n"
                    f"🇺🇿 {phrase['uz']}\n"
                    f"🔊 [{phrase['pronunciation']}]"
                )
                send_message(chat_id, text, get_main_menu())
            
            elif data == "help":
                send_message(
                    chat_id,
                    "❓ <b>Help</b>\n\n"
                    "Use the buttons below to learn English!\n"
                    "For full experience, open the Web App 🌐",
                    get_main_menu()
                )
            
            elif data == "back":
                send_message(chat_id, "🏠 Main Menu", get_main_menu())
            
            # Callback javobini yuborish
            requests.post(f"{API_URL}/answerCallbackQuery", json={"callback_query_id": callback["id"]})
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return "Error", 500

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)