import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

solve_the_task_callback = CallbackData("solve_the_task_callback", "file_path")
send_the_solve_callback = CallbackData('send_the_solve_callback', "file_path")
shedule_callback = CallbackData("shedule_callback", "file_path1")


def solve_the_task_creator(directory, id, n=0):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    start_n = n
    folders = os.listdir(directory)[n:]
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n = 0
    for file in folders:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=solve_the_task_callback.new(file_path=n)))
        if n == start_n + 90:
            files.add(
                InlineKeyboardButton(text=f'Ещё', callback_data=solve_the_task_callback.new(file_path='more')))
            files_in_folders[f'{id}nn'] = n
            return files
        n += 1

    files.add(InlineKeyboardButton(text='Прислать решение', callback_data=send_the_solve_callback.new(file_path=1)))
    return files

def shedule_creator(directory, id):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    folders = os.listdir(directory)
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n = 0
    for file in folders:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=shedule_callback.new(file_path1=n)))
        n+=1

    return files

