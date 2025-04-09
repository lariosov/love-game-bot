import app.const as const, app.keyboard as kb
import os, asyncio, random
from typing import List, Dict, Optional

# aiogram импорты
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery

# достаём переменные
from dotenv import main


main.load_dotenv()


# основные настройки бота и БД
bot = Bot(os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()


# Глобальный словарь для хранения активных игровых сессий
active_sessions: Dict[int, "GameSession"] = {}


class GameSession:
    def __init__(self):
        self.used_cards: List[int] = []  # Список использованных ID обычных карт
        self.used_penalty: List[int] = []  # Список использованных ID штрафов

    async def get_unique_card(self) -> Optional[Dict]:
        """Возвращает уникальную неиспользованную карту или None,
        если все карты использованы"""
        available_cards = [
            card_id for card_id in const.CARDS.keys() if card_id not in self.used_cards
        ]

        if not available_cards:
            return None

        card_id = random.choice(available_cards)
        card_data = const.CARDS[card_id]
        self.used_cards.append(card_id)

        return {"id": card_id, "theme": card_data["theme"], "qst": card_data["qst"]}

    async def get_unique_penalty(self) -> Optional[Dict]:
        """Возвращает уникальный неиспользованный штраф или None,
        если все штрафы использованы"""
        available_penalty = [
            p_id for p_id in const.PENALTY.keys() if p_id not in self.used_penalty
        ]

        if not available_penalty:
            return None

        penalty_id = random.choice(available_penalty)
        penalty_data = const.PENALTY[penalty_id]
        self.used_penalty.append(penalty_id)

        return {"id": penalty_id, "qst": penalty_data["qst"]}


def get_game_session(chat_id: int) -> GameSession:
    """Возвращает игровую сессию для указанного chat_id,
    создавая новую при необходимости"""
    if chat_id not in active_sessions:
        active_sessions[chat_id] = GameSession()
    return active_sessions[chat_id]


def end_game_session(chat_id: int) -> None:
    """Завершает игровую сессию для указанного chat_id"""
    if chat_id in active_sessions:
        del active_sessions[chat_id]


@dp.callback_query(F.data == "yes")
async def handle_yes(call: CallbackQuery):
    game_session = get_game_session(call.message.chat.id)
    card = await game_session.get_unique_card()

    if card:
        text = (
            f"🃏 Номер карточки: {card['id']}\n"
            f"🏷 Тема: {card['theme']}\n"
            f"📌 Задание: {card['qst']}\n\n"
            "Выполнишь? Или возьмёшь штраф?"
        )
        await call.message.answer(text, reply_markup=kb.game_answer())
    else:
        await call.message.answer("Все карты в этой игре уже использованы!")
        end_game_session(call.message.chat.id)
    await call.answer()


@dp.callback_query(F.data == "no")
async def handle_no(call: CallbackQuery):
    game_session = get_game_session(call.message.chat.id)
    penalty = await game_session.get_unique_penalty()

    if penalty:
        text = (
            f"💢 Штраф #{penalty['id']}\n"
            f"📛 Задание: {penalty['qst']}\n\n"
            f"Выполни этот штраф вместо основного задания!"
        )
        await call.message.answer(text, reply_markup=kb.penalty())
    else:
        await call.message.answer(
            "Все штрафы уже использованы! Придется выполнить основное задание 😈",
            reply_markup=kb.penalty()
        )
    await call.answer()


@dp.callback_query(F.data == "menu")
async def start_game(call: CallbackQuery):
    await call.message.answer(text="Прогресс игры сброшен!")
    await call.message.answer(text=const.END_GAME_TEXT,
                              reply_markup=kb.main_menu())
    end_game_session(call.message.chat.id)
    await call.answer()
    exit()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())  # отстаньте, это бест-практис
