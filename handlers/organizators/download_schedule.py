from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import organizators
from keyboards.inline import *
from keyboards.inline.schedule_maker import download_schedule_creator, schedule_callback
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states.all_state import *


@dp.message_handler(text='Добавить расписание', user_id=organizators)
async def add_schedule(message: types.Message):
    current_user_paths[message.from_user.id] = schedule
    await message.answer(
        text='Выберите группу:',
        reply_markup=download_schedule_creator(current_user_paths[message.from_user.id], message.from_user.id))


@dp.callback_query_handler(schedule_callback.filter(), user_id=organizators)
async def get_schedule(call: CallbackQuery, callback_data: dict):
    choosed_folder = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]
    current_user_paths[call.from_user.id] = rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'
    await GetSchedule.schedule.set()
    await call.message.answer(text='Добавьте файлы в одном письме')
    await GetSchedule.schedule.set()
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=GetSchedule.schedule, content_types=types.ContentType.DOCUMENT)
async def download_schedule(message: types.Message, state: FSMContext):
    await message.document.download(
        destination=
        rf'{current_user_paths[message.from_user.id]}\\{message.document.file_name}')
    await state.finish()
    await message.answer(text='Расписание добавлено')
