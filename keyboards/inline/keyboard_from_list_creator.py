from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

list_callback = CallbackData("list_callback", "elem_name")
take_task_callback = CallbackData('take_task_callback', 'take')
update_list_callback = CallbackData('update_list_callback', 'update_list')


def keyboard_creator(list, id):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    keyboard = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n = 0
    print(list)
    for element in list:
        files_in_folders[id].append(element)
        keyboard.add(InlineKeyboardButton(text=f'{element}', callback_data=list_callback.new(elem_name=n)))
        n+=1
    return keyboard


def take_a_task_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'Принять задачу', callback_data=take_task_callback.new(take=1)))
    keyboard.add(InlineKeyboardButton(text=f'Принять задачу', callback_data=take_task_callback.new(take=1)))
    return keyboard

def update_list_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'Обновить список в ожидании', callback_data=update_list_callback.new(update_list=1)))
    return keyboard