import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

download_tasks_callback = CallbackData("download_tasks_callback", "file_path")
download_tasks = CallbackData('download_tasks', 'file_path')


def download_tasks_creator(directory, id):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    folders = os.listdir(directory)
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n=0
    for file in folders:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=download_tasks_callback.new(file_path=n)))
        n += 1
    print(files_in_folders)

    files.add(InlineKeyboardButton(text='Загрузить задачи в эту папку', callback_data=download_tasks.new(file_path=1)))
    return files
