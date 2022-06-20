# Данный модуль отправляет основную навигационную клавиатуру для каждого типа пользователей

from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from keyboards.default import organizators_main_keyboard
from keyboards.default import students_main_keyboard
from keyboards.default import teachers_main_keyboard
from loader import dp


@dp.message_handler(Command('student_keyboard'), user_id=ADMINS)
async def show_student_keyboard(message: types.Message):
    await message.answer(text='Здравсвуйте!', reply_markup=students_main_keyboard)
    await message.answer(text='Клавиатура ученика активирована')


@dp.message_handler(Command('teacher_keyboard'), user_id=ADMINS)
async def show_teacher_keyboard(message: types.Message):
    await message.answer(text='Здравствуйте!', reply_markup=teachers_main_keyboard)
    await message.answer(text='Клавиатура учителя активирована')


@dp.message_handler(Command('organizators_keyboard'), user_id=ADMINS)
async def show_organizator_keyboard(message: types.Message):
    await message.answer(text='Здравствуйте!', reply_markup=organizators_main_keyboard)
    await message.answer(text='Клавиатура организатора активирована')
