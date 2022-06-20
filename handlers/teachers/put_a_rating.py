from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import teachers
from keyboards.inline import *
from keyboards.inline.check_the_solve_keyboard import check_the_solve_creator, check_the_solve_callback
from keyboards.inline.keyboard_from_list_creator import keyboard_creator, list_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp, db
from states.all_state import *
from utils.bot_utils import delete_last_message_call, delete_last_message
from utils.db_utils import columns_names


@dp.message_handler(text='Выставить баллы', user_id=teachers)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = solve_path
    await message.answer(text='Выберите ученика:',
                         reply_markup=check_the_solve_creator(solve_path, message.from_user.id))
    await PutRate.name.set()
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(check_the_solve_callback.filter(), state=PutRate.name, user_id=teachers)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)
    current_user_paths[call.from_user.id] = tasks_path
    allowed_disciplines = db.select_one_from_where(table_name='Учителя', column='Предметы', arg='chat_id', value=call.from_user.id)
    await state.update_data(name=files_in_folders[call.from_user.id][int(callback_data.get('file_path'))])
    await call.message.answer(text='Выберите предмет',
                              reply_markup=check_the_solve_creator(tasks_path, call.from_user.id, allowed_disciplines))
    await PutRate.discipline.set()
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(check_the_solve_callback.filter(), state=PutRate.discipline, user_id=teachers)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)
    discipline = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]
    await state.update_data(discipline=discipline)
    tasks = await columns_names(TableName=discipline)
    await call.message.answer(text='Выберите задание',
                              reply_markup=keyboard_creator(tasks[3:], call.from_user.id))
    await PutRate.task.set()
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(list_callback.filter(), state=PutRate.task, user_id=teachers)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)
    await state.update_data(task=files_in_folders[call.from_user.id][int(callback_data.get('elem_name'))])
    await call.message.answer(text='Введите оценку:')
    await PutRate.rate.set()
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=PutRate.rate, user_id=teachers)
async def get_a_rate(message: types.Message, state: FSMContext):
    await delete_last_message(message)
    data = await state.get_data()
    discipline = data.get('discipline')
    name = data.get('name')
    task = data.get('task')
    rate = message.text
    try:
        rate = int(rate)
    except:
        await message.answer(text='Необходимо ввести только число')
        return
    try:
        current_task_rate = int(db.select_one_from_where(
            column=task, table_name=discipline, arg='ФИО', value=name)[0])
    except:
        current_task_rate = 0
    db.update(data=rate - current_task_rate, FullName=name, TableName=discipline)
    db.update(data=rate - current_task_rate, FullName=name, TableName="Ученики")
    db.put_a_rating(FullName=name, task=task, rate=rate, TableName=discipline)
    await message.answer(text='Оценка сохранена')
    await state.finish()
