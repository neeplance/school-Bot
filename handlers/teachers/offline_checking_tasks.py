from aiogram import types

from data.config import *
from data.users_data import teachers, organizators
from keyboards.inline.keyboard_from_list_creator import keyboard_creator, list_callback, take_task_callback, \
    take_a_task_keyboard, update_list_keyboard, update_list_callback
from keyboards.inline.show_documents_keybord import show_document_creator, show_documents_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states.all_state import *
from utils.bot_utils import tasks_pending, delete_last_message, delete_last_message_call


@dp.message_handler(text='Проверка работ оффлайн', user_id=teachers|organizators)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    await SubmitTasks.auditory.set()
    await message.answer(
        text='Выберите аудиторию', reply_markup=keyboard_creator(auditories, message.from_user.id))
    current_user_paths[message.from_user.id] = {}
    await message.answer(text=await tasks_pending(), reply_markup=update_list_keyboard())
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(list_callback.filter(), state=SubmitTasks.auditory, user_id=teachers|organizators)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    current_user_paths[call.from_user.id]['auditory'] = files_in_folders[call.from_user.id][
        int(callback_data.get('elem_name'))]
    await call.message.answer(
        text='Выберите предмет:', reply_markup=show_document_creator(tasks_path, call.from_user.id))
    await SubmitTasks.discipline.set()
    await call.message.answer(text='Обновить список:', reply_markup=update_list_keyboard())
    await call.message.answer(text='Завершить', reply_markup=state_finish_creator())


@dp.callback_query_handler(show_documents_callback.filter(), state=SubmitTasks.discipline, user_id=teachers|organizators)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    current_user_paths[call.from_user.id]['discipline'] = files_in_folders[call.from_user.id][
        int(callback_data.get('file_path'))]
    discipline = current_user_paths[call.from_user.id]['discipline']
    auditory = current_user_paths[call.from_user.id]['auditory']
    try:
        submit_tasks_data[auditory][discipline] == 0

        await call.message.answer(
            text=f'Нажмите "Принять задачу", чтобы уменьшить количество задач в'
                 f' ожидании по предмету{callback_data.get("element")}'
                 f' в {current_user_paths[call.from_user.id]["auditory"]}', reply_markup=take_a_task_keyboard())
    except:
        await call.message.answer(text='В данной аудитории по данной дисциплине задачи отсутствуют\n\n'
                                  , reply_markup=update_list_keyboard())
    await call.message.answer(text='Завершить', reply_markup=state_finish_creator())


@dp.callback_query_handler(take_task_callback.filter(), state=SubmitTasks.discipline, user_id=teachers|organizators)
async def show_folders(call: types.CallbackQuery):
    await delete_last_message_call(call)
    auditory = current_user_paths[call.from_user.id]['auditory']
    discipline = current_user_paths[call.from_user.id]['discipline']
    submit_tasks_data[auditory][discipline] -= 1
    await call.message.answer(text='Завершить', reply_markup=state_finish_creator())


@dp.callback_query_handler(update_list_callback.filter(), state=SubmitTasks, user_id=teachers|organizators)
async def show_folders(call: types.CallbackQuery):
    await delete_last_message_call(call)
    try:
        await call.message.answer(text=await tasks_pending(), reply_markup=update_list_keyboard())
    except:
        await call.message.answer(text='Очередь отсутствует', reply_markup=update_list_keyboard())
    await call.message.answer(text='Завершить', reply_markup=state_finish_creator())
