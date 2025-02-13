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

@dp.message(lambda message: message.text == "🎮 Choose a game" or message.text == "🔙 Back to Main Menu")
async def choose_game(message: types.Message):
    await message.answer("Select a game:", reply_markup=game_menu)

@dp.message(lambda message: any(option in message.text for option in ["7 days", "30 days", "31 days", "Lifetime"]))
async def process_subscription_choice(message: types.Message):
    selected_option = message.text
    amount = selected_option.split(" - ")[1].replace("$", "")
    if amount in CRYPTO_PAYMENT_LINKS:
        payment_link = CRYPTO_PAYMENT_LINKS[amount]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="✅ I have paid")], [KeyboardButton(text="🔙 Back to Main Menu")]],
            resize_keyboard=True
        )
        await message.answer(f"You selected {selected_option}.
Pay using the link: {payment_link}
Once paid, click the button below.", reply_markup=keyboard)
    else:
        await message.answer("Invalid amount. Please choose a valid subscription option.")

@dp.message(lambda message: message.text == "✅ I have paid")
async def confirm_payment(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Contact Admin")], [KeyboardButton(text="🔙 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer("If you need any help, contact the admin.", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🔙 Back to Main Menu")
async def go_back_main_menu(message: types.Message):
    await message.answer("Returning to main menu:", reply_markup=main_menu)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
