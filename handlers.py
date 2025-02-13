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
        [KeyboardButton(text="🔙 Back to Main Menu")]
    ],
    resize_keyboard=True
)

# Cheat subscription prices
RUST_CHEAT_PRICES = {
    "Dopamine": {"7 days": 35, "30 days": 100},
    "Serotonin": {"30 days": 90},
    "Monolith": {"7 days": 35, "30 days": 70, "Lifetime": 750},
    "Quantum Private": {"31 days": 100},
    "Phantom": {"7 days": 40, "30 days": 120, "Lifetime": 800},
    "Overload": {"7 days": 50, "30 days": 140, "Lifetime": 900},
    "Nemesis": {"7 days": 45, "30 days": 130, "Lifetime": 850}
}

WAR_THUNDER_CHEAT_PRICES = {
    "Fecurity": {"30 days": 40},
    "Warchill": {"30 days": 55}
}

FORTNITE_CHEAT_PRICES = {
    "IGNITE": {"30 days": 110},
    "SHACK PRIVATE": {"30 days": 80}
}

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "No username"
    
    welcome_text = (
        "Welcome to GG Cheats – Your #1 Source for Game Cheats!\n\n"
        "Want to dominate your favorite game, stay ahead of the competition, and maximize your gaming experience? "
        "We offer reliable, undetectable, and regularly updated cheats for the most popular games.\n\n"
        "✅ Safety First – Minimal risk of bans\n"
        "✅ Instant Access – Get your cheat immediately after purchase\n"
        "✅ 24/7 Support – We're always here to help\n\n"
        "Choose your cheat and take your gameplay to the next level! 🚀"
    )
    
    admin_message = f"📢 New user started the bot!\n🆔 ID: {user_id}\n👤 Username: @{username}"
    await bot.send_message(ADMIN_ID, admin_message)
    await message.answer(welcome_text, reply_markup=main_menu)

@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer("Use the menu to select a game and see cheat options.")

@dp.message(lambda message: message.text in ["🎮 Choose a game", "🔙 Back to Main Menu"])
async def choose_game(message: types.Message):
    await message.answer("Select a game:", reply_markup=game_menu)

@dp.message(lambda message: message.text == "🎮 War Thunder")
async def show_war_thunder_cheats(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cheat)] for cheat in WAR_THUNDER_CHEAT_PRICES.keys()] + [[KeyboardButton(text="\U0001F519 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer("Select a cheat for War Thunder:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🎮 Fortnite")
async def show_fortnite_cheats(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cheat)] for cheat in FORTNITE_CHEAT_PRICES.keys()] + [[KeyboardButton(text="\U0001F519 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer("Select a cheat for Fortnite:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🎮 Rust")
async def show_rust_cheats(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cheat)] for cheat in RUST_CHEAT_PRICES.keys()] + [[KeyboardButton(text="\U0001F519 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer("Select a cheat for Rust:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🔙 Back to Main Menu")
async def go_back_main_menu(message: types.Message):
    await message.answer("Returning to main menu:", reply_markup=main_menu)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
