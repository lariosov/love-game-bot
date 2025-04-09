# основные импорты для вызова клавиатуры
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# вызываем клавиатуру и добавляем клавиши
# создаём MainMenu клавиатуру для добавления!
def main_menu():
    mainmenu = [
        [InlineKeyboardButton(text="Играть", callback_data="play")],
        [InlineKeyboardButton(text="Разработчик", url="t.me/lariosov")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=mainmenu)
