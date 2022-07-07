from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton

from app.handlers.kz import kz_start
from app.handlers.ru import ru_start
from app.utils import questions_ru, questions_kz


async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(text="Қазақ 🇰🇿"), KeyboardButton(text="Русский 🇷🇺")]
    keyboard.add(*buttons)
    await message.answer(
        "Сәлеметсіз бе, Qmarket техникалық қолдау ботына қош келдіңіз, ботпен жұмысты жалғастыру үшін тілді таңдаңыз\n\n"
        "Здравствуйте, вас приветствует бот технической поддержки Qmarket, выберете язык для продолжения работы с ботом",
        reply_markup=keyboard
    )


async def answer_to_questions(message: types.Message):
    if message.text in list(questions_ru.keys()):
        await message.answer(questions_ru[message.text])
    if message.text in list(questions_kz.keys()):
        await message.answer(questions_kz[message.text])


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(kz_start, Text(equals="Қазақ 🇰🇿"))
    dp.register_message_handler(ru_start, Text(equals="Русский 🇷🇺"))
    dp.register_message_handler(kz_start, Text(equals="⬅  Басты бетке оралу"))
    dp.register_message_handler(ru_start, Text(equals="⬅ ️Вернуться на главную страницу"))
    dp.register_message_handler(answer_to_questions, Text(startswith="Q:"))

