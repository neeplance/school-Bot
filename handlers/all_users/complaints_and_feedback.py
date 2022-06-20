import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import complaints
from data.config import feedback
from data.users_data import organizators, students, teachers
from keyboards.inline.state_finish import state_finish_creator
from loader import bot
from loader import dp
from states import Complaint


@dp.message_handler(text="Оставить жалобу", user_id=students | teachers)
async def make_complaint(message: types.Message):
    await message.answer('Отправьте свою жалобу в этот чат. Организаторы будут оповещены о её появлении и обязательно'
                         'на неё отреагируют!')
    await Complaint.complaint.set()
    await message.answer(text='Отмена', reply_markup=state_finish_creator())


@dp.message_handler(text='Оставить отзыв', user_id=students | teachers)
async def make_feedback(message: types.Message):
    await message.answer(text='Нам очень важно ваше мнение о нас! Чтобы поделиться им, перейдите по ссылке ниже:')
    await message.answer(text=feedback)


@dp.message_handler(state=Complaint.complaint)
async def complaiint_saver(message: types.Message, state: FSMContext):
    try:
        text = f'{students[message.from_user.id]}: {str(datetime.datetime.now())[:-7]}\n{message.text}\n\n'
    except:
        text = f'{teachers[message.from_user.id]}: {str(datetime.datetime.now())[:-7]}\n{message.text}\n\n'
    with open(complaints, 'a', encoding='utf-8') as f:
        f.write(text)
        f.close()
    await message.answer(text='Ваша жалоба принята')
    for admin in organizators:
        await bot.send_message(text="Появилась новая жалоба", chat_id=admin)
    await state.finish()


@dp.message_handler(text='Просмотр жалоб', user_id=organizators)
async def show_complaiints(message: types.Message):
    await bot.send_document(chat_id=message.from_user.id, document=open(complaints, 'rb'))
