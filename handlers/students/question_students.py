from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import *
from keyboards.inline.state_finish import state_finish_creator
from keyboards.inline.teachers_creator import teachers_creator, teachers_callback
from loader import dp
from states import Question
from utils.bot_utils import delete_last_message_call, delete_last_message


@dp.message_handler(text='Вопрос преподавателю', user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    await message.answer(
        text='Выберите преподавателя', reply_markup=teachers_creator(users['teachers'], message.from_user.id))


@dp.callback_query_handler(teachers_callback.filter(), user_id=students)
async def show_current_folder(call: CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    current_user_paths[call.from_user.id] = files_in_folders[call.from_user.id][int(callback_data.get('teacher'))]

    await call.message.answer(text='Введите вопрос:')
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())

    await Question.question.set()


@dp.message_handler(state=Question.question, user_id=students)
async def get_tasks(message: types.Message, state: FSMContext):
    await message.answer(text='Ваш вопрос был отправлен')
    await message.forward(chat_id=current_user_paths[message.from_user.id])
    await state.finish()
