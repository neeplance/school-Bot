from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


from data import *
from data.users_data import students
from keyboards.inline import *
from keyboards.inline.test_maker import question_creator, variants_callback, question_move_callback, \
    solve_the_test_creator, solve_the_test_callback
from loader import dp, db
from states import Test
from utils.bot_utils import delete_last_message_call, \
    delete_last_message
from utils.db_utils import rate_checker
from utils.test_creator import test_creator, name_creator


@dp.message_handler(text='Решить тест', user_id=students)
async def show_folders(message: types.Message):
    await delete_last_message(message)
    current_user_paths[message.from_user.id] = tests_path
    await message.answer(
        text='Выберите предмет',
        reply_markup=solve_the_test_creator(current_user_paths[message.from_user.id], message.from_user.id))


@dp.callback_query_handler(solve_the_test_callback.filter(file_path='more'))
async def show_current_folder(call: types.CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    await call.message.answer(
        text=f"Продолжение:",
        reply_markup=solve_the_test_creator(current_user_paths[call.from_user.id], call.from_user.id,
                                            n=files_in_folders[f'{call.from_user.id}nn']))


@dp.callback_query_handler(solve_the_test_callback.filter(), user_id=students)
async def show_current_folder(call: CallbackQuery, callback_data: dict):
    await delete_last_message_call(call)
    choosed_folder = files_in_folders[call.from_user.id][int(callback_data.get('file_path'))]
    if rf'{current_user_paths[call.from_user.id]}' == rf'{tests_path}':
        current_user_paths[f'{call.from_user.id}descipline'] = choosed_folder
    current_user_paths[call.from_user.id] = rf'{current_user_paths[call.from_user.id]}\{choosed_folder}'

    if os.path.isfile(current_user_paths[call.from_user.id]):
        current_user_paths[f'{call.from_user.id}test_name'] = name_creator(choosed_folder)
        test_name = name_creator(choosed_folder)
        if await rate_checker(FullName=students[call.from_user.id], task_name=test_name,
                              TableName=current_user_paths[f'{call.from_user.id}descipline']):
            await call.message.answer('Вы уже получили оценку за это задание')
            return

        await Test.test.set()
        current_user_paths[call.from_user.id] = test_creator(current_user_paths[call.from_user.id])
        current_user_paths[f'{call.from_user.id}n'] = 0
        current_user_paths[f'{call.from_user.id}answers'] = [0] * len(current_user_paths[call.from_user.id])
        await call.message.answer(text=current_user_paths[call.from_user.id][0][0],
                                  reply_markup=question_creator(current_user_paths[call.from_user.id][0]))
        return

    if os.path.isdir(current_user_paths[call.from_user.id]):
        await call.message.answer(
            text='Выберите раздел',
            reply_markup=solve_the_test_creator(current_user_paths[call.from_user.id], call.from_user.id))


@dp.callback_query_handler(variants_callback.filter(), state=Test.test, user_id=students)
async def download_files(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await delete_last_message_call(call)
    n = current_user_paths[f'{call.from_user.id}n']

    if callback_data.get('variant') == current_user_paths[call.from_user.id][n][-1]:
        current_user_paths[f'{call.from_user.id}answers'][n] = 1
    else:
        current_user_paths[f'{call.from_user.id}answers'][n] = 0

    if n == len(current_user_paths[call.from_user.id])-1:
        await call.message.answer(text='Это последний вопрос, вы можете изменить свои ответы иил завершить тест.')
        return


    current_user_paths[f'{call.from_user.id}n'] += 1
    n+=1
    qustion = current_user_paths[call.from_user.id][n]
    await call.message.answer(text=qustion[0], reply_markup=question_creator(qustion))



@dp.callback_query_handler(question_move_callback.filter(), state=Test.test, user_id=students)
async def download_files(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await delete_last_message_call(call)
    direction = int(callback_data.get('direction'))
    if direction == 0:
        discipline = current_user_paths[f'{call.from_user.id}descipline']
        await state.finish()
        rate_for_test = round(
            (sum(current_user_paths[f'{call.from_user.id}answers']) / len(current_user_paths[call.from_user.id])) * max_rate,
            2)
        await call.message.answer(text=f'Ваша оценка: {rate_for_test}')

        test_name = current_user_paths[f'{call.from_user.id}test_name']
        name = students[call.from_user.id]

        db.update(data=rate_for_test, FullName=name, TableName=discipline)
        db.update(data=rate_for_test, FullName=name, TableName="Ученики")

        db.put_a_rating_auto(TableName=discipline,
                             chat_id=call.from_user.id, task=current_user_paths[f'{call.from_user.id}test_name'],
                             rate=rate_for_test)
        db.update(data=rate_for_test, FullName=students[call.from_user.id], TableName=discipline)
        current_user_paths[f'{call.from_user.id}n'] = 0
        current_user_paths[f'{call.from_user.id}'] = 0
        current_user_paths[f'{call.from_user.id}answers'] = []
        return
    if current_user_paths[f'{call.from_user.id}n'] + direction <= len(current_user_paths[call.from_user.id])-1:
        current_user_paths[f'{call.from_user.id}n'] += direction
        n = current_user_paths[f'{call.from_user.id}n']
        qustion = current_user_paths[call.from_user.id][n]
        await call.message.answer(text=qustion[0], reply_markup=question_creator(qustion))
