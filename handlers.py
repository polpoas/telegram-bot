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

@dp.message(lambda message: message.text in RUST_CHEAT_PRICES.keys())
async def show_cheat_subscriptions(message: types.Message):
    cheat_name = message.text
    prices = RUST_CHEAT_PRICES[cheat_name]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{duration} - ${price}")] for duration, price in prices.items()] + [[KeyboardButton(text="🔙 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer(f"Subscription options for {cheat_name}:", reply_markup=keyboard)

@dp.message(lambda message: message.text in WAR_THUNDER_CHEAT_PRICES.keys())
async def show_wt_cheat_subscriptions(message: types.Message):
    cheat_name = message.text
    prices = WAR_THUNDER_CHEAT_PRICES[cheat_name]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{duration} - ${price}")] for duration, price in prices.items()] + [[KeyboardButton(text="🔙 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer(f"Subscription options for {cheat_name}:", reply_markup=keyboard)

@dp.message(lambda message: message.text in FORTNITE_CHEAT_PRICES.keys())
async def show_fortnite_cheat_subscriptions(message: types.Message):
    cheat_name = message.text
    prices = FORTNITE_CHEAT_PRICES[cheat_name]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{duration} - ${price}")] for duration, price in prices.items()] + [[KeyboardButton(text="🔙 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer(f"Subscription options for {cheat_name}:", reply_markup=keyboard)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
