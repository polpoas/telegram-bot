# handlers.py

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN, ADMIN_ID, CRYPTO_PAYMENT_LINKS
from database import init_db

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Logging
logging.basicConfig(level=logging.INFO)

# Main menu keyboard
main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎮 Choose a game")]],
    resize_keyboard=True
)

# Game selection keyboard
game_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 War Thunder")],
        [KeyboardButton(text="🎮 Fortnite")],
        [KeyboardButton(text="🎮 Rust")],
        [KeyboardButton(text="🔙 Back")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    welcome_text = (
        "Welcome to GG Cheats – Your #1 Source for Game Cheats!\n\n"
        "Want to dominate your favorite game, stay ahead of the competition, and maximize your gaming experience? "
        "We offer reliable, undetectable, and regularly updated cheats for the most popular games.\n\n"
        "✅ Safety First – Minimal risk of bans\n"
        "✅ Instant Access – Get your cheat immediately after purchase\n"
        "✅ 24/7 Support – We're always here to help\n\n"
        "Choose your cheat and take your gameplay to the next level! 🚀"
    )
    await message.answer(welcome_text, reply_markup=main_menu)

@dp.message(lambda message: message.text == "🎮 Choose a game" or message.text == "🔙 Back")
async def choose_game(message: types.Message):
    await message.answer("Select a game:", reply_markup=game_menu)

@dp.message(lambda message: message.text == "🎮 War Thunder")
async def show_war_thunder_cheats(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Fecurity")],
            [KeyboardButton(text="Warchill")],
            [KeyboardButton(text="🔙 Back")]
        ],
        resize_keyboard=True
    )
    await message.answer("Select a cheat for War Thunder:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🎮 Fortnite")
async def show_fortnite_cheats(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="IGNITE")],
            [KeyboardButton(text="SHACK PRIVATE")],
            [KeyboardButton(text="🔙 Back")]
        ],
        resize_keyboard=True
    )
    await message.answer("Select a cheat for Fortnite:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🎮 Rust")
async def show_rust_cheats(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Dopamine")],
            [KeyboardButton(text="Serotonin")],
            [KeyboardButton(text="🔙 Back")]
        ],
        resize_keyboard=True
    )
    await message.answer("Select a cheat for Rust:", reply_markup=keyboard)

@dp.message(lambda message: message.text in ["Dopamine", "Serotonin", "Fecurity", "Warchill", "IGNITE", "SHACK PRIVATE"])
async def show_payment_options(message: types.Message):
    selected_cheat = message.text
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="$35 - 1 Week")],
            [KeyboardButton(text="$75 - 1 Month")],
            [KeyboardButton(text="$300 - 1 Year")],
            [KeyboardButton(text="🔙 Back")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"You selected {selected_cheat}. Choose a subscription period:", reply_markup=keyboard)

@dp.message(lambda message: message.text in ["$35 - 1 Week", "$75 - 1 Month", "$300 - 1 Year"])
async def process_payment(message: types.Message):
    amount = message.text.split(" ")[0].replace("$", "")
    payment_link = CRYPTO_PAYMENT_LINKS[amount].format(order_id=message.chat.id)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ I have paid")],
            [KeyboardButton(text="🔙 Back")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Pay using the link: {payment_link}\nOnce paid, click the button below.", reply_markup=keyboard)

@dp.message(lambda message: message.text == "✅ I have paid")
async def confirm_payment(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Contact Admin")],
            [KeyboardButton(text="🔙 Back")]
        ],
        resize_keyboard=True
    )
    await message.answer("If you need any help, contact the admin.", reply_markup=keyboard)

@dp.message(lambda message: message.text == "📞 Contact Admin")
async def contact_admin(message: types.Message):
    await message.answer(f"You can contact the administrator here: @cheatGGadmin")

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
