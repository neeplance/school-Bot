import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import *
from data.users_data import organizators
from keyboards.inline.events_creator import events_org_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states.all_state import *
from utils.bot_utils import delete_last_message_call, delete_last_message


@dp.callback_query_handler(events_org_callback.filter(variant='create'), user_id=organizators)
async def create_event(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await delete_last_message_call(call)

    await call.message.answer(text='Введите название мероприятия:')
    await GetEvent.event_name.set()
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=GetEvent.event_name, user_id=organizators)
async def take_create_name(message: types.Message, state: FSMContext):
    await delete_last_message(message)
    await state.update_data(name=message.text)
    await message.answer(
        text='Введите описание мероприятия:')
    await GetEvent.event_text.set()
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=GetEvent.event_text, user_id=organizators)
async def take_event_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')

    text = message.text
    await message.answer(text='Мероприятие сохранено')
    await state.finish()
    with open(current_user_paths[message.from_user.id], 'r', encoding='utf-8') as f:
        data = json.load(f)
        data[f'{name}'] = {'Описание': f'{text}', 'Участники': [], 'Организаторы': []}
        f.close()
    with open(current_user_paths[message.from_user.id], 'w', encoding='utf-8') as f:
        f.write(f'{json.dumps(data, ensure_ascii=False, indent=4)}')
        f.close()
