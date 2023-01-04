from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton

from app.handlers.kz import kz_start
from app.handlers.ru import ru_start
from app.utils import questions_ru, questions_kz
from app.db import get_database
from app.config_reader import load_config

import re

collection_name = get_database()
global_bot = None
config = load_config("config/bot.ini")

lessons_dict = {
    'Урок 1: Вводное видео': {"url": "https://drive.google.com/file/d/1wIsdReBbjLUammutN7dA8wzjTWZuT9n7/view?usp=share_link",
               "description": f"Вводное видео\n\nГосударство оказывает фермерам поддержку в виде субсидий. Посмотри видео о том, что такое субсидии, кто их может получать и что для этого нужно сделать.\nДля тех, кто желает получить подробную информацию по всем мерам государственной поддержки с обратной связью от эксперта, доступен платный курс"},
    'Урок 2: Подготовка документов': {"url": "https://drive.google.com/file/d/1zTbVugiY9HnJJFYZqHeE8iD1p5dJ08bM/view?usp=share_link",
               "description": f"Подготовка документов\n\nПодготовка документов – неотъемлемая часть процесса подачи заявок на субсидии. Именно документы подтверждают основание для получения субсидии. Посмотри видео и узнай, какие основные требования предъявляются к документам.\nДокументоведение – это целая наука, поэтому на полном курсе данной теме отведен целый урок, где вы подробно узнаете все тонкости по подготовке пакета документов."},
    'Урок 3: Оцифровка': {"url": "https://drive.google.com/file/d/1acw4gWljDBpVoL4ksNThwoUg3IAJe98B/view?usp=share_link",
               "description": f"Оцифровка\n\nДля получения субсидий по направлению растениеводства необходимо наличие земельных угодий, которые оцифрованы. Что нужно знать при оцифровке и угодий и создании севооборотов, посмотри в видео.\nЕсли ты желаешь на живом примере увидеть, как оцифровывается земельное угодье, получить обратную связь от эксперта по своему хозяйству, запишись на полный курс."},
    'Урок 4: Расчет суммы': {"url": "https://drive.google.com/file/d/1_hzLBwIe5l1K6r4ykzSSx2H26Wk5iziZ/view?usp=share_link",
               "description": f"Расчет суммы\n\nСумма субсидий, которую может получить фермер, зависит от множества факторов. Часто бывает так, что фермер планирует одну сумму, а фактически получает другую.  Что влияет на сумму субсидий посмотри в видео.\nМатематические расчеты и формулы порой написаны очень сложно, на полном курсе мы рассказываем простым языком о сложном, ты с легкостью сможешь посчитать сколько субсидий может получить твоя организация, также ты получишь обратную связь от эксперта для этого пройди полный курс с сопровождением."},
    'Урок 5: Подача заявки': {"url": "https://drive.google.com/file/d/1TzDM7te0yuGeMUXGhMmrpAOBiI9ICw7X/view?usp=share_link",
               "description": f"Подача заявки\n\nПодача заявки – легкий процесс, если вы знаете основные этапы и уже подготовили всю необходимую информацию. Остается только внести данные из документов в заявку и прикрепить необходимый пакет документов. Как это сделать правильно смотри в видео.\nНа полном курсе мы разбираем подробно каждое направление субсидирования (удобрения, семена, пестициды, ставка вознаграждения, инвестиционные субсидии и т.д) с учетом всех нюансов, которые могут появиться, также все обучающиеся получают обратную связь от эксперта по любому вопросу, который касается субсидирования, для этого пройди полный курс."},
    'Урок 6: Заключительное видео': {"url": "https://drive.google.com/file/d/16M4WSywAKd_6Vsv2hdQiZJMGGjFhuogC/view?usp=share_link",
               "description": f"Заключительное видео\n\nВажно помнить, что субсидии – это не спасательный круг, а приятный кэшбэк или бонус для успешной компании. Посмотри видео о том, что влияет на успех в получении субсидий.\n«Кадры решают все!» - эта фраза актуальна в любое время, а квалифицированные кадры тем более. С помощью наших курсов вы повысите уровень ваших специалистов, что позволит выйти на новый уровень доходности. Выбери свой курс и повысь уровень своих знаний!"},
    'Купить полный курс': {'description': 'Чтобы получить доступ к полному курсу, можете написать Динаре: @dinara_moldagaipova'}
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
                if not re.match("^\+77\d{9}$", message.text):
                    await message.answer("Ошибка, введите номер телефона согласно шаблону: +77XXXXXXXXX")
                else:
                    collection_name.update_one({'_id': chat_id['_id']}, {"$set": {'phone': message.text}}, upsert=False)
                    await global_bot.send_message(config.tg_bot.admin1_id, f"Данные нового пользователя бота:\nИмя: {chat_id['full_name']}\nНомер: {message.text}")
                    await global_bot.send_message(config.tg_bot.admin2_id,
                                                  f"Данные нового пользователя бота:\nИмя: {chat_id['full_name']}\nНомер: {message.text}")
                    await global_bot.send_message(config.tg_bot.admin3_id,
                                                  f"Данные нового пользователя бота:\nИмя: {chat_id['full_name']}\nНомер: {message.text}")
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
            url = lessons_dict[message.text].get("url", None)
            if url:
                await message.answer(url)
            await message.answer(lessons_dict[message.text]["description"], reply_markup=keyboard)
        else:
            await message.answer("Ошибка!")
    else:
        await message.answer("Сперва вы должны заполнить ваши данные!")

# async def answer_to_questions(message: types.Message):
#     if message.text in list(questions_ru.keys()):
#         await message.answer(questions_ru[message.text])
#     if message.text in list(questions_kz.keys()):
#         await message.answer(questions_kz[message.text])


def register_handlers_common(dp: Dispatcher, bot):
    global global_bot
    global_bot = bot
    dp.register_message_handler(lessons, Text(equals="Купить полный курс"))
    dp.register_message_handler(lessons, Text(startswith="Урок"))
    dp.register_message_handler(cmd_start)

    # dp.register_message_handler(kz_start, Text(equals="Қазақ 🇰🇿"))
    # dp.register_message_handler(ru_start, Text(equals="Русский 🇷🇺"))
    # dp.register_message_handler(kz_start, Text(equals="⬅  Басты бетке оралу"))
    # dp.register_message_handler(ru_start, Text(equals="⬅ ️Вернуться на главную страницу"))
    # dp.register_message_handler(answer_to_questions, Text(startswith="Q:"))

