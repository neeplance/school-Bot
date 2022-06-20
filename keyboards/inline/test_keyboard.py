import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

test_cb = CallbackData("check_the_solve_callback", "file_path")


def test_keyboard(list, id, n=0):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    start_n=n
    folders = list[n:]
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []

    for file in folders:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=test_cb.new(file_path=n)))
        if n==start_n+90:
            files.add(
                InlineKeyboardButton(text=f'Ещё', callback_data=test_cb.new(file_path='more')))
            files_in_folders[f'{id}nn'] = n
            return files
        n+=1
    return files