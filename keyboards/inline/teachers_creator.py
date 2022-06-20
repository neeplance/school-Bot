from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

teachers_callback = CallbackData("teachers_callback", "teacher")


def teachers_creator(teachers, id):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    keyboard = InlineKeyboardMarkup()

    files_in_folders[id] = []
    n = 0
    for id_t, teacher in teachers.items():
        files_in_folders[id].append(id_t)
        keyboard.add(InlineKeyboardButton(text=f'{teacher}', callback_data=teachers_callback.new(teacher=n)))
        n+=1
    return keyboard
