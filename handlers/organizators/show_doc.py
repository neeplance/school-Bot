
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import users, organizators
from keyboards.inline import *
from keyboards.inline.state_finish import state_finish_creator
from keyboards.inline.users_sheet_creator import *
from loader import bot
from loader import dp
from states import ShowDocs
from utils.bot_utils import delete_last_message_call


# С помощью данного модуля пользователи могу запросить ифнормацию о другиъ пользователях
# Нажать "Получить информацию о пользователе" -> Выбрать тип пользователя -> Выбрать ФИО ользователя, о котором
# необходима информация


@dp.message_handler(text='Получить документы', user_id=organizators)
async def show_user_categories(message: types.Message):
    await ShowDocs.doc.set()
    await message.answer(text='Выберите тип пользователя', reply_markup=choose_user_type)
    await message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(user_callback_doc.filter(user_name='more'), state=ShowDocs.doc)
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    await call.message.answer('Продолжение:',
                              reply_markup=users_sheet_keyboard_doc(users[callback_data.get('user_type')].values(),
                                                                    call.from_user.id,
                                                                    n=files_in_folders[f'{call.from_user.id}nn']))
    await call.message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(type_user_callback.filter(), state=ShowDocs.doc)
async def show_users(call: CallbackQuery, callback_data: dict):
    current_user_paths['choosed_type'] = users[callback_data.get('user_type')].values()
    if callback_data.get('user_type') == 'students':
        current_user_paths[call.from_user.id] = students_doc_path
    elif callback_data.get('user_type') == 'teachers':
        current_user_paths[call.from_user.id] = teachers_doc_path
    else:
        current_user_paths[call.from_user.id] = organizators_doc_path

    await call.answer(cache_time=60)
    await call.message.answer('Выберите пользователя',
                              reply_markup=users_sheet_keyboard_doc(users[callback_data.get('user_type')].values(),
                                                                    call.from_user.id))
    await call.message.answer(
        text='Отмена', reply_markup=state_finish_creator())


@dp.callback_query_handler(user_callback_doc.filter(), state=ShowDocs.doc, user_id=organizators)
async def show_current_folder(call: CallbackQuery, callback_data: dict, state: FSMContext):
    choosed_folder = files_in_folders[call.from_user.id][int(callback_data.get('user_name'))]
    print('gee')
    print(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}')
    if os.path.isdir(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'):
        print('dir')
        current_user_paths[call.from_user.id] = rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'
        list = os.listdir(current_user_paths[call.from_user.id])
        await call.message.answer(
            text='Выберите файл',
            reply_markup=users_sheet_keyboard_doc(list, call.from_user.id))
    else:
        await bot.send_document(chat_id=call.from_user.id,
                                document=open(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}', 'rb'))
    await call.message.answer(
        text='Отмена', reply_markup=state_finish_creator())
    await state.finish()