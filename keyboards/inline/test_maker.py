import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

variants_callback = CallbackData("variants_callback", "variant")
question_move_callback = CallbackData('question_move_callback', 'direction')

solve_the_test_callback = CallbackData("solve_the_test_callback", "file_path")


def solve_the_test_creator(directory, id, n=0):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    start_n = n
    folders = os.listdir(directory)[n:]
    files = InlineKeyboardMarkup()
    files_in_folders[id] = []
    n = 0
    for file in folders:
        files_in_folders[id].append(file)
        files.add(InlineKeyboardButton(text=f'{file}', callback_data=solve_the_test_callback.new(file_path=n)))
        if n == start_n + 90:
            files.add(
                InlineKeyboardButton(text='Ещё', callback_data=solve_the_test_callback.new(file_path='more')))
            files_in_folders[f'{id}nn'] = n
            return files
        n += 1

    return files

def question_creator(question):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    variants = InlineKeyboardMarkup()
    for variant in question[1:-1]:
        variants.add(InlineKeyboardButton(text=f'{variant}', callback_data=variants_callback.new(variant=f'{variant}')))
    variants.add(InlineKeyboardButton(text="Предыдущий вопрос", callback_data=question_move_callback.new(direction=-1)))
    variants.add(
        InlineKeyboardButton(text="Следующий вопрос", callback_data=question_move_callback.new(direction=1)))
    variants.add(
        InlineKeyboardButton(text="Завершить тест", callback_data=question_move_callback.new(direction=0)))
    return variants

