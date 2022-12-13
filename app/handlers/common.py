from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton

from app.handlers.kz import kz_start
from app.handlers.ru import ru_start
from app.utils import questions_ru, questions_kz
from app.db import get_database

collection_name = get_database()

lessons_dict = {
    'Урок 1': "https://youtube.com/shorts/-4caNQEEaFY?feature=share",
    'Урок 2': "https://youtube.com/shorts/-4caNQEEaFY?feature=share",
    'Урок 3': "https://youtube.com/shorts/-4caNQEEaFY?feature=share",
    'Урок 4': "https://youtube.com/shorts/-4caNQEEaFY?feature=share",
    'Урок 5': "https://youtube.com/shorts/-4caNQEEaFY?feature=share",
}

async def cmd_start(message: types.Message):
    chat_id = collection_name.find_one({"chat_id": message.chat.id})

    if chat_id:
        if chat_id['full_name']:
            if chat_id['phone']:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for name in list(lessons_dict.keys()):
                    keyboard.add(name)
                await message.answer("Уроки", reply_markup=keyboard)
            else:
                collection_name.update_one({'_id': chat_id['_id']}, {"$set": {'phone': message.text}}, upsert=False)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for name in list(lessons_dict.keys()):
                    keyboard.add(name)
                await message.answer("Уроки", reply_markup=keyboard)
        else:
            collection_name.update_one({'_id': chat_id['_id']}, {"$set": {'full_name': message.text}}, upsert=False)
            await message.answer("Ваш номер: ")
    else:
        collection_name.insert_one({'chat_id': message.chat.id, "phone": None, "full_name": None})
        await message.answer(
        "Здравствуйте, добро пожаловать на курсы по Агросубсидированию! Для доступа к материалам курса, отправьте пожалуйста ваши данные")
        await message.answer("Ваше имя: ")


async def lessons(message: types.Message):
    chat_id = collection_name.find_one({"chat_id": message.chat.id})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in list(lessons_dict.keys()):
        keyboard.add(name)

    if chat_id:
        if message.text in lessons_dict.keys():
            await message.answer(lessons_dict[message.text])
            await message.answer(message.text, reply_markup=keyboard)
        else:
            await message.answer("Ошибка!")
    else:
        await message.answer("Сперва вы должны заполнить ваши данные!")

# async def answer_to_questions(message: types.Message):
#     if message.text in list(questions_ru.keys()):
#         await message.answer(questions_ru[message.text])
#     if message.text in list(questions_kz.keys()):
#         await message.answer(questions_kz[message.text])


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(lessons, Text(startswith="Урок"))
    dp.register_message_handler(cmd_start)
    # dp.register_message_handler(kz_start, Text(equals="Қазақ 🇰🇿"))
    # dp.register_message_handler(ru_start, Text(equals="Русский 🇷🇺"))
    # dp.register_message_handler(kz_start, Text(equals="⬅  Басты бетке оралу"))
    # dp.register_message_handler(ru_start, Text(equals="⬅ ️Вернуться на главную страницу"))
    # dp.register_message_handler(answer_to_questions, Text(startswith="Q:"))

