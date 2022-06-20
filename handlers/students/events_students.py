import json

from aiogram import types

from data.config import *
from data.users_data import students
from keyboards.inline.events_creator import events_creator, events_callback, approve, approve_callback
from loader import dp
from utils.bot_utils import delete_last_message, delete_last_message_call


@dp.message_handler(text='Мероприятия', user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = events
    await message.answer(
        text='Выберите мероприятие', reply_markup=events_creator(events))


@dp.callback_query_handler(events_callback.filter(), user_id=students)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    with open(current_user_paths[call.from_user.id], 'r', encoding='utf-8') as f:
        events_data = json.load(f)
        f.close()
    event_name = callback_data.get('event')
    if event_name == '0':
        await call.message.answer(text='Выберите мероприятие',
                                  reply_markup=events_creator(current_user_paths[call.from_user.id]))
        return
    await call.message.answer(
        text=f"{event_name}:\n\n{events_data[callback_data.get('event')]['Описание']}",
        reply_markup=approve(event_name))



@dp.callback_query_handler(approve_callback.filter(), user_id=students)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    with open(current_user_paths[call.from_user.id], 'r', encoding='utf-8') as f:
        events_data = json.load(f)
        f.close()

    if students[call.from_user.id] in events_data[f'{callback_data.get("event")}']['Участники']:
        await call.message.answer(text='Вы уже были записаны на мероприятие')
        return
    with open(current_user_paths[call.from_user.id], 'w', encoding='utf-8') as f:
        events_data[f'{callback_data.get("event")}']['Участники'].append(students[call.from_user.id])
        f.write(f'{json.dumps(events_data, ensure_ascii=False, indent=4)}')
        f.close()

    await call.message.answer(text='Вы были записаны')