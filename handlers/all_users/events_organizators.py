# Отвечает за создание мероприятий и добавлении учеников в мероприятия

import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import *
from data.users_data import students, organizators, teachers
from keyboards.inline.check_the_solve_keyboard import check_the_solve_creator
from keyboards.inline.events_creator import add_to_event, \
    add_to_event_callback, events_creator_org, events_org_callback, event_info_or_add_st
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states import GetEvent
from utils.bot_utils import delete_last_message_call, delete_last_message



@dp.message_handler(text='Мероприятия', user_id=organizators)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = events
    await message.answer(
        text='Выберите мероприятие:', reply_markup=events_creator_org(events))


@dp.callback_query_handler(events_org_callback.filter(variant='choose'), user_id=organizators)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)
    event_name = callback_data.get('event')
    await call.message.answer(
        text='Что вы хотите сделать с мероприятием?', reply_markup=event_info_or_add_st(event_name))
    await state.finish()


@dp.callback_query_handler(events_org_callback.filter(variant='info'), user_id=organizators)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    event_name = callback_data.get('event')
    with open(current_user_paths[call.from_user.id], 'r', encoding='utf-8') as f:
        data = json.load(f)

        f.close()
    students_sheet = '\n* '.join(map(str, data[event_name]['Участники']))
    await call.message.answer(
        text=f"Описание:\n\n{data[event_name]['Описание']}\n\n"
             f"Участники:\n\n{students_sheet}")


@dp.callback_query_handler(add_to_event_callback.filter(student='more'))
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    event_name = callback_data.get('event')
    await delete_last_message_call(call)
    await call.message.answer(
        text=f"Продолжение",
        reply_markup=add_to_event(students.values(), call.from_user.id, event_name, n=files_in_folders[f'{call.from_user.id}nn']))


@dp.callback_query_handler(events_org_callback.filter(variant='add st'), user_id=organizators)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    event_name = callback_data.get('event')
    await call.message.answer(
        text='Выберите студента', reply_markup=add_to_event(students.values(), event_name, call.from_user.id))



@dp.callback_query_handler(add_to_event_callback.filter(student='team'))
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    await call.message.answer(text='Напишите в одном сообщении ФИО всех уыеников, которые составят одну команду')
    await GetEvent.team.set()
    print(callback_data.get('event'))
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())
    files_in_folders[call.from_user.id] = callback_data.get('event')



@dp.callback_query_handler(add_to_event_callback.filter(), user_id=organizators)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    student_name = files_in_folders[call.from_user.id][int(callback_data.get("student"))]
    with open(current_user_paths[call.from_user.id], 'r', encoding='utf-8') as f:
        data = json.load(f)
        if student_name in data[f'{files_in_folders[call.from_user.id][-1]}']['Участники']:
            await call.message.answer(text='Студент уже записан на мероприятие')
            f.close()
            return
        data[f'{files_in_folders[call.from_user.id][-1]}']['Участники'].append(student_name)
    with open(current_user_paths[call.from_user.id], 'w', encoding='utf-8') as f:
        f.write(f'{json.dumps(data, ensure_ascii=False, indent=4)}')
        f.close()

    await call.message.answer(text='Студент был записан')


@dp.message_handler(state=GetEvent.team)
async def show_current_folder(message: types.Message, state: FSMContext):
    await delete_last_message(message)
    student_names = message.text
    with open(current_user_paths[message.from_user.id], 'r', encoding='utf-8') as f:
        data = json.load(f)
        data[f'{files_in_folders[message.from_user.id]}']['Участники'].append(student_names)
        f.close()
    with open(current_user_paths[message.from_user.id], 'w', encoding='utf-8') as f:
        f.write(f'{json.dumps(data, ensure_ascii=False, indent=4)}')
        f.close()

    await message.answer(text='Команда была записана')
    await state.finish()