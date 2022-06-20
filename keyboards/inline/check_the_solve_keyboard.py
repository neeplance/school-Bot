import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders
from data.users_data import disciplines

check_the_solve_callback = CallbackData("check_the_solve_callback", "file_path")


def check_the_solve_creator(directory, id, allowed_disciplines='x'):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    print(allowed_disciplines)
    print(allowed_disciplines)
    if allowed_disciplines == 'x':
        print(allowed_disciplines)
        folders = os.listdir(directory)
    else:
        print(allowed_disciplines)
        folders = allowed_disciplines
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n=0
    for file in folders:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=check_the_solve_callback.new(file_path=n)))
        n+=1
    return files