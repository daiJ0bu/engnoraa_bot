import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# 🔑 Telegram bot tokeningni shu joyga yoz
TOKEN = "8175905001:AAEiUDItp344S3MmFGQIzInVO_nnPwhDSjs"

# ✅ Yangi versiyada shunday qilib beriladi:
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

@dp.message()
async def start(message: types.Message):
    if message.text == "/start":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🌐 Open Engnoraa",
                        web_app=WebAppInfo(url="https://engnoraa.vercel.app")  # sayting linkini yoz
                    )
                ]
            ]
        )
        await message.answer(
            "👋 Welcome to <b>Engnoraa English</b>!\nLearn, play and test your English 🌟",
            reply_markup=keyboard
        )

async def main():
    print("🤖 Engnoraa bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
