from aiogram import types

from data.config import *
from data.users_data import students
from keyboards.inline.keyboard_from_list_creator import keyboard_creator, list_callback
from keyboards.inline.show_documents_keybord import show_document_creator, show_documents_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states.all_state import *
from utils.bot_utils import delete_last_message_call, delete_last_message


@dp.message_handler(text='Сдать работу', user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    await SubmitTasks.auditory.set()
    await message.answer(
        text='Выберите аудиторию', reply_markup=keyboard_creator(auditories, message.from_user.id))
    current_user_paths[message.from_user.id] = {}
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(list_callback.filter(), state=SubmitTasks.auditory, user_id=students)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    current_user_paths[call.from_user.id]['auditory'] = files_in_folders[call.from_user.id][int(callback_data.get('elem_name'))]
    await call.message.answer(
        text='Выберите предмет:', reply_markup=show_document_creator(tasks_path, call.from_user.id))
    await SubmitTasks.discipline.set()
    await call.message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(show_documents_callback.filter(), state=SubmitTasks.discipline, user_id=students)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    current_user_paths[call.from_user.id]['discipline'] = \
        files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]
    await call.message.answer(
        text='Введите число задач, которые вы хотите сдать:\n(строго одно число!)')
    await SubmitTasks.number_of_tasks.set()
    await call.message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=SubmitTasks.number_of_tasks, user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    auditory = current_user_paths[message.from_user.id]['auditory']
    discipline = current_user_paths[message.from_user.id]['discipline']
    print(submit_tasks_data)

    try:
        submit_tasks_data[auditory][discipline] += int(message.text)
        print(submit_tasks_data)
    except KeyError:
        try:
            submit_tasks_data[auditory][discipline] = int(message.text)
            print(submit_tasks_data, 1)
        except KeyError:
            submit_tasks_data[auditory] = {}
            submit_tasks_data[auditory][discipline] = int(message.text)
            print(submit_tasks_data, 2)
    await message.answer(
        text='Ответ принят, можете добавить задачи по другому предмету:',
        reply_markup=show_document_creator(tasks_path, message.from_user.id))
    await SubmitTasks.discipline.set()
    await message.answer(
        text='Отмена', reply_markup=state_finish_creator())
