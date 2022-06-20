# С помощью данного модуля пользователи могу запросить ифнормацию о другиъ пользователях
# Нажать "Получить информацию о пользователе" -> Выбрать тип пользователя -> Выбрать ФИО ользователя, о котором
# необходима информация

from aiogram import types
from aiogram.types import CallbackQuery

from data import current_user_paths, students_doc_path, teachers_doc_path, organizators_doc_path
from data.users_data import users, organizators
from keyboards.inline.users_sheet_creator import *
from loader import dp, db
from utils.bot_utils import delete_last_message_call


@dp.message_handler(text='Получить информацию о пользователе', user_id=organizators)
async def show_user_categories(message: types.Message):
    await message.answer(text='Выберите тип пользователя', reply_markup=choose_user_type)


@dp.callback_query_handler(user_callback_doc.filter(user_name='more'))
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    await call.message.answer('Продолжение',
                              reply_markup=users_sheet_keyboard_doc(users[callback_data.get('user_type')].values(),
                                                                    call.from_user.id,
                                                                    n=files_in_folders[f'{call.from_user.id}nn']))


@dp.callback_query_handler(type_user_callback.filter())
async def show_users(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    current_user_paths['choosed_type'] = users[callback_data.get('user_type')].values()
    if callback_data.get('user_type') == 'students':
        current_user_paths[call.from_user.id] = students_doc_path
    elif callback_data.get('user_type') == 'teachers':
        current_user_paths[call.from_user.id] = teachers_doc_path
    else:
        current_user_paths[call.from_user.id] = organizators_doc_path
    await call.message.answer('Выберите пользователя',
                              reply_markup=users_sheet_keyboard_doc(users[callback_data.get('user_type')].values(),
                                                                    call.from_user.id))


@dp.callback_query_handler(user_callback_doc.filter())
async def send_user_datas(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    if current_user_paths[call.from_user.id] == students_doc_path:
        user_date = db.select_student(ФИО=files_in_folders[call.from_user.id][int((callback_data.get('user_name')))])
        print(user_date)
        await call.message.answer(f'ФИО: {user_date[2]}\nГруппа: {user_date[4]}\nКоличество баллов: {user_date[6]}\n'
                                  f'Телефон: {user_date[3]}\ntelegram_id: {user_date[0]}\n'
                                  f'nickname: {user_date[6]}\n')
    elif current_user_paths[call.from_user.id] == teachers_doc_path:
        user_date = db.select_from_where(table_name="Учителя", arg='ФИО', value=files_in_folders[call.from_user.id][
            int((callback_data.get('user_name')))])[0]
        await call.message.answer(
            f'ФИО: {user_date[2]}\nПредметы: {user_date[4]}\nТелефон: {user_date[3]}\ntelegram_id: {user_date[0]}\n'
            f'nickname: {user_date[1]}\n')
    else:
        user_date = \
        db.select_from_where(table_name="Организаторы", arg='ФИО', value=files_in_folders[call.from_user.id][
            int((callback_data.get('user_name')))])[0]
        await call.message.answer(
            f'ФИО: {user_date[2]}\n Телефон: {user_date[3]}\ntelegram_id: {user_date[0]}\n'
            f'nickname: {user_date[1]}\n')
