from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as fmt
from app.utils import questions_ru, available_options_ru


async def ru_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_options_ru:
        keyboard.add(name)
    await message.answer("Вы выбрали русский язык\n\n Выберите один из пунктов:", reply_markup=keyboard)


async def seller_call_center_info(message: types.Message):
    await message.answer("Контакты колл центра АО «ҚазАзот»:\n+7 777 420 1081\n+7 771 949 9119")
    return


async def get_video(message: types.Message):
    await message.answer(f"{fmt.hide_link('https://www.youtube.com/watch?v=VK4dRxkqDJM&t=755s')}Обучающее видео ", parse_mode=types.ParseMode.HTML)
    return


async def qmarket_call_center_info(message: types.Message):
    await message.answer("Контакты колл центра QMARKET:\n+7 777 448 36 36")
    return


async def faq_questions(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in list(questions_ru.keys()):
        keyboard.add(name)
    await message.answer("Выберите вопрос:", reply_markup=keyboard)


def register_handlers_ru(dp: Dispatcher):
    dp.register_message_handler(ru_start, commands="ru")
    dp.register_message_handler(seller_call_center_info, Text(equals="Узнать колл центр продавцов"))
    dp.register_message_handler(faq_questions, Text(equals="Ответы на часто задаваемые вопросы"))
    dp.register_message_handler(get_video, Text(equals="Посмотреть обучающие видео"))
    dp.register_message_handler(qmarket_call_center_info, Text(equals="Узнать колл центр Qmarketa"))