import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

show_documents_callback = CallbackData("show_documents_callback", "file_path")


def show_document_creator(directory, id):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    folders = os.listdir(directory)
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n = 0
    for file in folders[:50]:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=show_documents_callback.new(file_path=n)))
        n+=1
    return files

