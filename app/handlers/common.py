from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton

from app.handlers.kz import kz_start
from app.handlers.ru import ru_start
from app.utils import questions_ru, questions_kz
from app.db import get_database
from app.config_reader import load_config
from app.lessons import lessons, course_titles

import re

collection_name = get_database()
global_bot = None
config = load_config("config/bot.ini")



async def cmd_start(message: types.Message):
    chat_id = collection_name.find_one({"chat_id": message.chat.id})

    if chat_id:
        if chat_id['full_name']:
            if chat_id['phone']:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for course_title in course_titles:
                    keyboard.add(course_title)
                await message.answer("Курсы", reply_markup=keyboard)
            else:
                if not re.match("^(\+77\d{9}|87\d{9})$", message.text):
                    await message.answer("Ошибка, введите номер телефона согласно шаблону: +77XXXXXXXXX или 87XXXXXXXXX")
                else:
                    collection_name.update_one({'_id': chat_id['_id']}, {"$set": {'phone': message.text}}, upsert=False)
                    await global_bot.send_message(config.tg_bot.admin1_id, f"Данные нового пользователя бота:\nИмя: {chat_id['full_name']}\nНомер: {message.text}")
                    await global_bot.send_message(config.tg_bot.admin2_id,
                                                  f"Данные нового пользователя бота:\nИмя: {chat_id['full_name']}\nНомер: {message.text}")
                    await global_bot.send_message(config.tg_bot.admin3_id,
                                                  f"Данные нового пользователя бота:\nИмя: {chat_id['full_name']}\nНомер: {message.text}")
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for course_title in course_titles:
                        keyboard.add(course_title)
                    await message.answer("Курсы", reply_markup=keyboard)
        else:
            collection_name.update_one({'_id': chat_id['_id']}, {"$set": {'full_name': message.text}}, upsert=False)
            await message.answer("Ваш номер: ")
    else:
        collection_name.insert_one({'chat_id': message.chat.id, "phone": None, "full_name": None})
        await message.answer(
        "Здравствуйте, добро пожаловать на курсы по Агросубсидированию! Для доступа к материалам курса, отправьте пожалуйста ваши данные")
        await message.answer("Ваше имя: ")


async def get_lesson(message: types.Message):
    founded = False
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chat_id = collection_name.find_one({"chat_id": message.chat.id})
    if chat_id:
        for lesson in lessons:
            if lesson['title'] == message.text:
                course_type = lesson['course_type']
                url = lesson.get("url")
                description = lesson.get("description")
                founded = True
                break
        else:
            keyboard.add('Вернуться к выбору курсов ↩️')
            await message.answer("Ошибка!", reply_markup=keyboard)

        if founded:
            for lesson in lessons:
                if course_type == lesson['course_type'] or lesson['course_type'] == 'Общий':
                    keyboard.add(lesson['title'])
            if url:
                await message.answer(url)
            await message.answer(description, reply_markup=keyboard)
    else:
        await message.answer("Сперва вы должны заполнить ваши данные!")


async def get_courses(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lesson in lessons:
        if message.text == lesson['course_type'] or lesson['course_type'] == 'Общий':
            keyboard.add(lesson['title'])

    await message.answer("Уроки", reply_markup=keyboard)


async def courses_list(message: types.Message):
    chat_id = collection_name.find_one({"chat_id": message.chat.id})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for course_title in course_titles:
        keyboard.add(course_title)
    if chat_id:
        await message.answer("Курсы", reply_markup=keyboard)
    else:
        await message.answer("Сперва вы должны заполнить ваши данные!")


def register_handlers_common(dp: Dispatcher, bot):
    global global_bot
    global_bot = bot
    dp.register_message_handler(get_lesson, Text(equals="Купить полный курс 💵"))
    dp.register_message_handler(courses_list, Text(equals="Вернуться к выбору курсов ↩️"))
    dp.register_message_handler(get_lesson, Text(startswith="Урок"))
    dp.register_message_handler(get_courses, Text(startswith="Курсы"))
    dp.register_message_handler(cmd_start)

    # dp.register_message_handler(kz_start, Text(equals="Қазақ 🇰🇿"))
    # dp.register_message_handler(ru_start, Text(equals="Русский 🇷🇺"))
    # dp.register_message_handler(kz_start, Text(equals="⬅  Басты бетке оралу"))
    # dp.register_message_handler(ru_start, Text(equals="⬅ ️Вернуться на главную страницу"))
    # dp.register_message_handler(answer_to_questions, Text(startswith="Q:"))

