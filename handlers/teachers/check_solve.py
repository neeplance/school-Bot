from aiogram import types
from aiogram.types import CallbackQuery

from data import *
from data.users_data import teachers
from keyboards.inline import *
from keyboards.inline.check_the_solve_keyboard import check_the_solve_callback, check_the_solve_creator
from loader import dp, bot
from utils.bot_utils import delete_last_message, delete_last_message_call


@dp.message_handler(text='Проверить решение задачи', user_id=teachers)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = solve_path
    await message.answer(
        text='Выберите ученика', reply_markup=check_the_solve_creator(solve_path, message.from_user.id),)


@dp.callback_query_handler(check_the_solve_callback.filter(), user_id=teachers)
async def show_current_folder(call: CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    choosed_folder = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]


    if os.path.isfile(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'):
        await bot.send_document(chat_id=call.from_user.id,
                                document=open(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}', 'rb'))

    if os.path.isdir(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'):
        current_user_paths[call.from_user.id] = rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'
        await call.message.answer(text='Выберите задание', reply_markup=check_the_solve_creator(
            current_user_paths[call.from_user.id], call.from_user.id))
    await delete_last_message_call(call)
