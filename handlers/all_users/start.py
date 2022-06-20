from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.users_data import students, teachers, organizators
from keyboards.default import students_main_keyboard, teachers_main_keyboard, organizators_main_keyboard
from loader import dp


@dp.message_handler(CommandStart(), user_id=students)
async def bot_start(message: types.Message):
    await message.answer(text=f"Здравствуйте, {students[message.from_user.id]}!", reply_markup=students_main_keyboard)
    await message.answer(text=f"Бот готов к использованию")


@dp.message_handler(CommandStart(), user_id=teachers)
async def bot_start(message: types.Message):
    await message.answer(text=f"Здравствуйте, {teachers[message.from_user.id]}!", reply_markup=teachers_main_keyboard)
    await message.answer(text=f"Бот готов к использованию")


@dp.message_handler(CommandStart(), user_id=organizators)
async def bot_start(message: types.Message):
    await message.answer(
        text=f"Здравствуйте, {organizators[message.from_user.id]}!", reply_markup=organizators_main_keyboard)
    await message.answer(text=f"Бот готов к использованию")
