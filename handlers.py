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
    keyboard=[[KeyboardButton(text="\U0001F3AE Choose a game")]],
    resize_keyboard=True
)

# Game selection keyboard
game_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="\U0001F3AE War Thunder")],
        [KeyboardButton(text="\U0001F3AE Fortnite")],
        [KeyboardButton(text="\U0001F3AE Rust")],
        [KeyboardButton(text="\U0001F519 Back to Main Menu")]
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
    await message.answer("Welcome! Choose a game to see available cheats.", reply_markup=game_menu)

@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer("Use the menu to select a game and see cheat options.")

@dp.message(lambda message: message.text in ["\U0001F3AE Choose a game", "\U0001F519 Back to Main Menu"])
async def choose_game(message: types.Message):
    await message.answer("Select a game:", reply_markup=game_menu)

@dp.message(lambda message: message.text in RUST_CHEAT_PRICES.keys())
async def show_rust_cheat_prices(message: types.Message):
    cheat_name = message.text
    prices = RUST_CHEAT_PRICES[cheat_name]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{period} - ${price}")] for period, price in prices.items()] + [[KeyboardButton(text="\U0001F519 Back to Game Selection")]],
        resize_keyboard=True
    )
    await message.answer(f"Subscription options for {cheat_name}:", reply_markup=keyboard)

@dp.message(lambda message: message.text in WAR_THUNDER_CHEAT_PRICES.keys())
async def show_war_thunder_cheat_prices(message: types.Message):
    cheat_name = message.text
    prices = WAR_THUNDER_CHEAT_PRICES[cheat_name]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{period} - ${price}")] for period, price in prices.items()] + [[KeyboardButton(text="\U0001F519 Back to Game Selection")]],
        resize_keyboard=True
    )
    await message.answer(f"Subscription options for {cheat_name}:", reply_markup=keyboard)

@dp.message(lambda message: message.text in FORTNITE_CHEAT_PRICES.keys())
async def show_fortnite_cheat_prices(message: types.Message):
    cheat_name = message.text
    prices = FORTNITE_CHEAT_PRICES[cheat_name]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{period} - ${price}")] for period, price in prices.items()] + [[KeyboardButton(text="\U0001F519 Back to Game Selection")]],
        resize_keyboard=True
    )
    await message.answer(f"Subscription options for {cheat_name}:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "\U0001F519 Back to Game Selection")
async def go_back_to_game_selection(message: types.Message):
    await message.answer("Returning to game selection:", reply_markup=game_menu)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
