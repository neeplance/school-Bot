from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import *
from data.users_data import students, teachers, organizators
from keyboards.inline.state_finish import state_finish_creator
from loader import dp
from states import GetDocs


@dp.message_handler(text='Загрузить документы', user_id=organizators | students | teachers)
async def download_docs(message: types.Message):
    await message.answer(text='Загрузите документы одним сообщением. \n '
                              'Внимание! прикрепляйте только через "прикрепить файл, даже если это фото')
    await GetDocs.doc.set()
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(state=GetDocs.doc, content_types=types.ContentType.DOCUMENT)
async def download_files(message: types.Message, state: FSMContext):
    if message.from_user.id in students:
        path = rf'{students_doc_path}\\{students[message.from_user.id]}'
    elif message.from_user.id in teachers:
        path = rf'{teachers_doc_path}\\{teachers[message.from_user.id]}'
    elif message.from_user.id in organizators:
        path = rf'{organizators_doc_path}\\{organizators[message.from_user.id]}'

    await message.document.download(
        destination=rf'{path}\\{message.from_user.id}{message.document.file_name}')
    await state.finish()
    await message.answer(text='Ваши документы сохранены!')
