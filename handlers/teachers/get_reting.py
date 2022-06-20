from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import teachers, organizators
from keyboards.inline import *
from keyboards.inline.check_the_solve_keyboard import check_the_solve_creator, check_the_solve_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp, bot
from states.all_state import *
from utils.bot_utils import delete_last_message_call, delete_last_message, delete_last_2_message_call
from utils.db_utils import return_rate, save_data_to_excel


@dp.message_handler(text='Баллы ученика', user_id=teachers|organizators)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = solve_path
    await message.answer(text='Выберите ученика:',
                         reply_markup=check_the_solve_creator(solve_path, message.from_user.id))
    await GetRate.name.set()
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(check_the_solve_callback.filter(), state=GetRate.name, user_id=teachers|organizators)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)
    current_user_paths[call.from_user.id] = tasks_path
    await state.update_data(name=files_in_folders[call.from_user.id][int(callback_data.get('file_path'))])
    await call.message.answer(text='Выберите предмет',
                              reply_markup=check_the_solve_creator(tasks_path, call.from_user.id))
    await GetRate.discipline.set()
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(check_the_solve_callback.filter(), state=GetRate.discipline, user_id=teachers|organizators)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)
    discipline = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]
    data = await state.get_data()
    name = data.get('name')

    await call.message.answer(text=await return_rate(FullName=name, TableName=discipline), )
    await state.finish()


@dp.message_handler(text='Общая успеваемость', user_id=teachers|organizators)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    await message.answer(text='Выберите предмет',
                         reply_markup=check_the_solve_creator(tasks_path, message.from_user.id))
    await GetAllRate.rate.set()
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(check_the_solve_callback.filter(), state=GetAllRate.rate, user_id=teachers|organizators)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_2_message_call(call)
    discipline = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]
    file = await save_data_to_excel(TableName=discipline, path_to_save=discipline_rate_path)

    await bot.send_document(chat_id=call.from_user.id, document=open(file, 'rb'))
    await state.finish()
