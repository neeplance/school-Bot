import os.path
import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import teachers, organizators
from keyboards.inline import *
from keyboards.inline.state_finish import state_finish_creator
from loader import dp, db, bot
from states.all_state import *
from utils.bot_utils import delete_last_message_call, delete_last_message
from utils.test_creator import name_creator


@dp.message_handler(text='Добавить задачу', user_id=teachers|organizators)
async def show_folders(message: types.Message):
    current_user_paths[message.from_user.id] = tasks_path
    await delete_last_message(message)
    await message.answer(
        text='Выберите предмет:',
        reply_markup=download_tasks_creator(current_user_paths[message.from_user.id], message.from_user.id))


@dp.message_handler(text='Добавить тест', user_id=teachers|organizators)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = tests_path
    await message.answer(
        text='Выберите предмет:',
        reply_markup=download_tasks_creator(current_user_paths[message.from_user.id], message.from_user.id))


@dp.callback_query_handler(download_tasks_callback.filter(), user_id=teachers|organizators)
async def show_current_folder(call: CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    choosed_folder = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]

    if rf'{current_user_paths[call.from_user.id]}' == rf'{tests_path}' \
            or rf'{current_user_paths[call.from_user.id]}' == rf'{tasks_path}':
        current_user_paths[f'{call.from_user.id}descipline'] = choosed_folder

    if os.path.isdir(f'{current_user_paths[call.from_user.id]}\{choosed_folder}'):
        current_user_paths[call.from_user.id] = f'{current_user_paths[call.from_user.id]}\{choosed_folder}'
        await call.message.answer(
            text='Выберите раздел',
            reply_markup=download_tasks_creator(current_user_paths[call.from_user.id], call.from_user.id))
    else:
        await bot.send_document(chat_id=call.from_user.id,
                                document=open(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}', 'rb'))

@dp.callback_query_handler(download_tasks.filter(), user_id=teachers|organizators)
async def get_tasks(call: CallbackQuery):
    await delete_last_message_call(call)
    await call.message.answer(text='Добавьте задания в одном письме')
    await GetTasks.task.set()
    await call.message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=GetTasks.task, content_types=types.ContentType.DOCUMENT)
async def download_files(message: types.Message, state: FSMContext):
    task_name = name_creator(message.document.file_name)
    discipline = current_user_paths[f'{message.from_user.id}descipline']
    await delete_last_message(message)
    try:
        db.add_column(column_name=task_name, TableName=discipline)
    except sqlite3.OperationalError:
        await message.answer(text='Задание с таким названием уже есть в базе данных этого предмета')
        await state.finish()
        return

    await message.document.download(
        destination=rf'{current_user_paths[message.from_user.id]}\{message.document.file_name}')
    await state.finish()
    await message.answer(text='Ваши задания сохранены!')



