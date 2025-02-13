import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN, ADMIN_ID, CRYPTO_PAYMENT_LINKS
from database import init_db

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎮 Choose a game")]],
    resize_keyboard=True
)

game_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 War Thunder")],
        [KeyboardButton(text="🎮 Fortnite")],
        [KeyboardButton(text="🎮 Rust")],
        [KeyboardButton(text="🔙 Back to Main Menu")]
    ],
    resize_keyboard=True
)

cheat_menus = {
    "🎮 War Thunder": ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Fecurity")], [KeyboardButton(text="🚀 Warchill")],
                  [KeyboardButton(text="🔙 Back to Game Selection")]],
        resize_keyboard=True
    ),
    "🎮 Fortnite": ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🎯 IGNITE")], [KeyboardButton(text="🎯 SHACK PRIVATE")],
                  [KeyboardButton(text="🔙 Back to Game Selection")]],
        resize_keyboard=True
    ),
    "🎮 Rust": ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔥 Dopamine")], [KeyboardButton(text="🔥 Serotonin")],
                  [KeyboardButton(text="🔥 Monolith")], [KeyboardButton(text="🔥 Quantum Private")],
                  [KeyboardButton(text="🔙 Back to Game Selection")]],
        resize_keyboard=True
    )
}

cheat_prices = {
    "🚀 Fecurity": {"30 days": 40}, "🚀 Warchill": {"30 days": 55},
    "🎯 IGNITE": {"30 days": 110}, "🎯 SHACK PRIVATE": {"30 days": 80},
    "🔥 Dopamine": {"7 days": 35, "30 days": 100}, "🔥 Serotonin": {"30 days": 90},
    "🔥 Monolith": {"7 days": 35, "30 days": 70, "Lifetime": 750}, "🔥 Quantum Private": {"31 days": 100}
}

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Welcome to GG Cheats – Your #1 Source for Game Cheats!

"
        "Want to dominate your favorite game, stay ahead of the competition, and maximize your gaming experience? "
        "We offer reliable, undetectable, and regularly updated cheats for the most popular games.

"
        "✅ Safety First – Minimal risk of bans
"
        "✅ Instant Access – Get your cheat immediately after purchase
"
        "✅ 24/7 Support – We're always here to help

"
        "Choose your cheat and take your gameplay to the next level! 🚀",
        reply_markup=main_menu
    )

@dp.message()
async def debug_message(message: types.Message):
    await message.answer(f"Received: {message.text}")

@dp.message(lambda message: message.text == "🎮 Choose a game" or message.text == "🔙 Back to Main Menu")
async def choose_game(message: types.Message):
    await message.answer("Select a game:", reply_markup=game_menu)

@dp.message(lambda message: message.text in cheat_menus.keys())
async def show_cheats(message: types.Message):
    await message.answer(f"Select a cheat for {message.text}:", reply_markup=cheat_menus[message.text])

@dp.message(lambda message: message.text in cheat_prices.keys())
async def show_subscription_options(message: types.Message):
    selected_cheat = message.text
    prices = cheat_prices[selected_cheat]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{duration} - ${price}")] for duration, price in prices.items()] +
                 [[KeyboardButton(text="🔙 Back to Game Selection")]],
        resize_keyboard=True
    )
    await message.answer(f"Subscription options for {selected_cheat}:", reply_markup=keyboard)

@dp.message(lambda message: " - " in message.text)
async def process_subscription_choice(message: types.Message):
    try:
        amount = message.text.split(" - ")[1].replace("$", "").strip()
        if amount in CRYPTO_PAYMENT_LINKS:
            payment_link = CRYPTO_PAYMENT_LINKS[amount]
            keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="✅ I have paid")], [KeyboardButton(text="🔙 Back to Main Menu")]],
                resize_keyboard=True
            )
            await message.answer(f"You selected {message.text}.\nPay using the link: {payment_link}\nOnce paid, click the button below.", reply_markup=keyboard)
        else:
            await message.answer("Invalid amount. Please choose a valid subscription option.")
    except IndexError:
        await message.answer("Invalid selection. Please choose a valid subscription option.")

@dp.message(lambda message: message.text == "✅ I have paid")
async def confirm_payment(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Contact Admin")], [KeyboardButton(text="🔙 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer("If you need any help, contact the admin.", reply_markup=keyboard)

@dp.message(lambda message: message.text == "📞 Contact Admin")
async def contact_admin(message: types.Message):
    await message.answer("You can contact the administrator here: @cheatGGadmin")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Contact Admin")], [KeyboardButton(text="🔙 Back to Main Menu")]],
        resize_keyboard=True
    )
    await message.answer("If you need any help, contact the admin.", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🔙 Back to Game Selection")
async def go_back_game_selection(message: types.Message):
    await message.answer("Returning to game selection:", reply_markup=game_menu)

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
