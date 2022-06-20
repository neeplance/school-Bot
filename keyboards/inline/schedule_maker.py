import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

schedule_callback = CallbackData("schedule_callback", "file_path")


def download_schedule_creator(directory, id):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    folders = os.listdir(directory)
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n = 0
    for file in folders:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=schedule_callback.new(file_path=n)))
        n += 1

    return files
