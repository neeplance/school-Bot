import asyncio
import datetime

import aiogram.types

from data import submit_tasks_data
from loader import bot


async def delete_last_message(message: aiogram.types.Message):
    # Скрывает последнюю отправленную клавиатуру
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    except:
        pass


async def delete_last_message_call(call: aiogram.types.CallbackQuery):
    # Скрывает последнюю отправленную клавиатуру
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
    except:
        pass


async def delete_last_2_message_call(call: aiogram.types.CallbackQuery):
    # Скрывает последнюю отправленную клавиатуру
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    except:
        pass


async def delete_last_2_message(message: aiogram.types.Message):
    # Скрывает последнюю отправленную клавиатуру
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 2)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    except:
        pass


def delete_zero(arr):
    for i in range(0, len(arr)):
        if int(arr[i]) < 10:
            arr[i] = arr[i].split('0')[-1]
            if arr[i] == '':
                arr[i] = 0
    return arr


async def secunds_creator(date, time):
    # Возвращает количество оставшихся секунд до указанного времени
    time = time.split(':')

    date = date.split('.')[::-1]
    date = delete_zero(date)
    time = delete_zero(time)
    date = date + time
    plane_date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), 0)
    delay = int((plane_date - datetime.datetime.now()).total_seconds())
    return delay


async def send_reminder(users, text, date, time):
    delay = await secunds_creator(date, time)
    await asyncio.sleep(delay)
    for id in users:
        try:
            await bot.send_message(chat_id=id, text=text)
        except:
            continue


async def tasks_pending():
    text = 'Задачи в ожидании:'
    for auditory in submit_tasks_data:
        text += f'\n{auditory}:\n'
        for descipline in submit_tasks_data[auditory]:
            text += f'{descipline}:{submit_tasks_data[auditory][descipline]}\n'
    return text
