from aiogram import types
from aiogram.types import CallbackQuery

from data import *
from data.users_data import organizators, students, teachers
from keyboards.inline import *
from loader import dp
from utils.test_creator import file_reader


@dp.message_handler(text='Получить расписание', user_id=organizators | students | teachers)
async def get_schedule(message: types.Message):
    current_user_paths[message.from_user.id] = schedule
    await message.answer(
        text='Выберите группу',
        reply_markup=shedule_creator(current_user_paths[message.from_user.id], message.from_user.id))


@dp.callback_query_handler(shedule_callback.filter(), user_id=organizators | students | teachers)
async def show_schedule(call: CallbackQuery, callback_data: dict):
    choosed_folder = files_in_folders[call.from_user.id][int(callback_data.get('file_path1'))]
    current_user_paths[call.from_user.id] = rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'

    print('shedule')

    if os.path.isdir(current_user_paths[call.from_user.id]):
        await call.message.answer(
            text='Выберите файл',
            reply_markup=shedule_creator(current_user_paths[call.from_user.id], call.from_user.id))
    else:
        schedule = file_reader(current_user_paths[call.from_user.id])
        await call.message.answer(text=schedule)
