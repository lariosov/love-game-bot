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


# меню для игры
def game_answer():
    gameanswer = [
        [InlineKeyboardButton(text="Сделано", callback_data="yes")],
        [InlineKeyboardButton(text="Отказ", callback_data="no")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Главное меню", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=gameanswer)
