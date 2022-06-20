from aiogram import types

from data import *
from data.users_data import students
from keyboards.inline import *
from loader import dp
from utils.bot_utils import delete_last_message


@dp.message_handler(text='Мои решения', user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = rf'{solve_path}\\{students[message.from_user.id]}'
    await message.answer(text='Ваши решения:',
        reply_markup=solve_the_task_creator(current_user_paths[message.from_user.id], message.from_user.id))
