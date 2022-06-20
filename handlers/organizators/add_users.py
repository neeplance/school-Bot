from aiogram import types
from aiogram.dispatcher import FSMContext

from data import *
from data.users_data import organizators
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states.all_state import *
from utils.db_utils import add_users


@dp.message_handler(text='Добавить учеников', user_id=organizators)
async def get_students_on(message: types.Message):
    await message.answer(
        text='Загрузите список учеников в виде файла эксель:')
    await GetStudents.students.set()
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=GetStudents.students, content_types=types.ContentType.DOCUMENT)
async def get_students(message: types.Message, state: FSMContext):
    document = f'{add_users_path}\{message.document.file_name}'
    await message.document.download(destination=document)
    await add_users(document=document, TableName='Ученики')
    await state.finish()
    await message.answer(text='Пользователи добавлены')


@dp.message_handler(text='Добавить учителей', user_id=organizators)
async def get_teachers_on(message: types.Message):
    await message.answer(
        text='Загрузите список учителей в виде файла эксель:')
    await GetTeachers.teachers.set()
    await message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=GetTeachers.teachers, content_types=types.ContentType.DOCUMENT)
async def get_teachers(message: types.Message, state: FSMContext):
    document = f'{add_users_path}\{message.document.file_name}'
    await message.document.download(destination=document)
    await add_users(document=document, TableName='Учителя')
    await state.finish()
    await message.answer(text='Пользователи добавлены')
