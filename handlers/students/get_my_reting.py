from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import students
from keyboards.inline import *
from keyboards.inline.check_the_solve_keyboard import check_the_solve_creator, check_the_solve_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states.all_state import *
from utils.bot_utils import delete_last_message_call, delete_last_message
from utils.db_utils import return_rate


@dp.message_handler(text='Мои оценки', user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = tasks_path
    await message.answer(text='Выберите предмет',
                         reply_markup=check_the_solve_creator(tasks_path, message.from_user.id))
    await message.answer(
        text='Отмена', reply_markup=state_finish_creator())
    await GetMyRate.rate.set()


@dp.callback_query_handler(check_the_solve_callback.filter(), state=GetMyRate.rate, user_id=students)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)
    discipline = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]
    await call.message.answer(text=await return_rate(FullName=students[call.from_user.id], TableName=discipline))
    await state.finish()
