from aiogram import types
from aiogram.dispatcher import FSMContext

from data.users_data import users, organizators
from keyboards.inline import choose_user_type, type_user_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states.all_state import *
from utils.bot_utils import send_reminder


@dp.message_handler(text='Создать рассылку', user_id=organizators)
async def show_folders(message: types.Message):
    await GetReminder.users_type.set()
    await message.answer(
        text='Выберите тип пользователей, которые получат рассылку:', reply_markup=choose_user_type)
    await message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(type_user_callback.filter(), state=GetReminder.users_type, user_id=organizators)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(users_type=callback_data.get('user_type'))
    await call.message.answer(text='Введите текст сообщения:', reply_markup=state_finish_creator())
    await call.message.answer(
        text='Отмена', reply_markup=state_finish_creator())
    await GetReminder.reminder.set()


@dp.message_handler(state=GetReminder.reminder, user_id=organizators)
async def show_current_folder(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(text='Введите дату рассылки в формате дд.мм.гг:', reply_markup=state_finish_creator())
    await message.answer(
        text='Отмена', reply_markup=state_finish_creator())
    await GetReminder.date.set()


@dp.message_handler(state=GetReminder.date, user_id=organizators)
async def show_current_folder(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer(text='Введите время рассылки в формате час:минуты:', reply_markup=state_finish_creator())
    await message.answer(
        text='Отмена', reply_markup=state_finish_creator())
    await GetReminder.time.set()


@dp.message_handler(state=GetReminder.time, user_id=organizators)
async def show_current_folder(message: types.Message, state: FSMContext):
    date = await state.get_data()
    users_id = users[date.get('users_type')].keys()
    text = date.get('text')
    date = date.get('date')
    time = message.text
    print(users_id, text, date, time)
    await message.answer(text='Напоминание было создано!')
    await state.finish()
    await send_reminder(users=users_id, text=text, date=date, time=time)

