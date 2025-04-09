import app.const as const, app.database as db
import app.keyboard as kb
import os, asyncio, subprocess

# aiogram импорты
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# достаём переменные
from dotenv import main

main.load_dotenv()


"""
DO NOT EDIT MANUALY
Telegram: @lariosov
"""


# основные настройки бота и БД
bot = Bot(os.getenv("BOT_TOKEN"),
          parse_mode=ParseMode.HTML)
dp = Dispatcher()


# обрабатываем команду старт
@dp.message(CommandStart())
async def start(message: Message) -> None:
    await bot.send_message(
        chat_id=message.chat.id,
        text=const.WELCOME_TEXT,
        reply_markup=kb.main_menu(),
    )


# обработка меню
@dp.callback_query(F.data == "menu")
async def menu(call: CallbackQuery):
    await call.message.answer(reply_markup=kb.main_menu())
    await call.answer()


# игра начинается
@dp.callback_query(F.data == "play")
async def game_rules(call: CallbackQuery):
    await call.message.answer(text=const.RULES,
                              reply_markup=kb.ready())
    await call.answer(
        "Ознакомьтесь с правилами!",
        show_alert=True,
    )
    subprocess.call(['python3', 'game.py'])


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())  # отстаньте, это бест-практис
