from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import *
from data.users_data import *
from keyboards.inline import *
from keyboards.inline.state_finish import state_finish_creator
from loader import dp, bot
from states import GetSolve
from utils.bot_utils import delete_last_message_call, delete_last_message


@dp.message_handler(text='Решить задачу', user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = tasks_path
    await message.answer(
        text='Выберите предмет',
        reply_markup=solve_the_task_creator(current_user_paths[message.from_user.id], message.from_user.id))


@dp.callback_query_handler(solve_the_task_callback.filter(file_path='more'))
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    await call.message.answer(
        text=f"Продолжение:",
        reply_markup=solve_the_task_creator(current_user_paths[call.from_user.id], call.from_user.id,
                                            n=files_in_folders[f'{call.from_user.id}nn']))


@dp.callback_query_handler(solve_the_task_callback.filter(), user_id=students)
async def show_current_folder(call: CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    choosed_folder = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]

    if os.path.isdir(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'):
        current_user_paths[call.from_user.id] = rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'
        await call.message.answer(
            text='Выберите раздел',
            reply_markup=solve_the_task_creator(current_user_paths[call.from_user.id], call.from_user.id))
    else:
        await bot.send_document(chat_id=call.from_user.id,
                                document=open(rf'{current_user_paths[call.from_user.id]}\{choosed_folder}', 'rb'))


@dp.callback_query_handler(send_the_solve_callback.filter(), user_id=students)
async def get_tasks(call: CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    await call.message.answer(text='Добавьте задачи в одном письме')
    await call.message.answer(text='Отмена', reply_markup=state_finish_creator())
    await GetSolve.solve.set()


@dp.message_handler(state=GetSolve.solve, content_types=types.ContentType.DOCUMENT, user_id=students)
async def download_files(message: types.Message, state: FSMContext):
    await delete_last_message(message)
    await message.document.download(
        destination=rf'{solve_path}\\{students[message.from_user.id]}\\{message.document.file_name}')

    await state.finish()
    await message.answer(text='Ваше решение сохранено!')
