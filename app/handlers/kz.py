from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as fmt


from app.utils import available_options_kz, questions_kz


async def kz_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_options_kz:
        keyboard.add(name)
    await message.answer("Төмендегі бір нұсқаны таңдаңыз:", reply_markup=keyboard)


async def seller_call_center_info(message: types.Message):
    await message.answer("«ҚазАзот» АҚ байланыс орталығының байланыстары:\n+7 777 420 1081\n+7 771 949 9119")
    return


async def get_video(message: types.Message):
    await message.answer(f"{fmt.hide_link('https://www.youtube.com/watch?v=ZxD57oRVB6g')}Тапсырысты рәсімдеу", parse_mode=types.ParseMode.HTML)
    await message.answer(f"{fmt.hide_link('https://www.youtube.com/watch?v=pWGWKYKzAKA')}Тапсырысты төлеу", parse_mode=types.ParseMode.HTML)
    return


async def qmarket_call_center_info(message: types.Message):
    await message.answer("QMARKET байланыс орталығының байланыстары:\n+7 777 448 36 36")
    return


async def faq_questions(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("⬅  Басты бетке оралу")
    for name in list(questions_kz.keys()):
        keyboard.add(name)
    await message.answer("Сұрақты таңдаңыз:", reply_markup=keyboard)


def register_handlers_kz(dp: Dispatcher):
    dp.register_message_handler(kz_start, commands="kz")
    dp.register_message_handler(seller_call_center_info, Text(equals="📞 Сатушылардың байланыс орталықтарын біліңіз"))
    dp.register_message_handler(faq_questions, Text(equals="❓ Жиі қойылатын сұрақтарға жауаптар"))
    dp.register_message_handler(get_video, Text(equals="▶️ Нұсқаулық бейнелерді қараңыз"))
    dp.register_message_handler(qmarket_call_center_info, Text(equals="📞 Qmarketa байланыс орталығын табыңыз"))
