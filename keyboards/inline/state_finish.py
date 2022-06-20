
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

state_finish_callback = CallbackData('state_finish_callback', 'finish')



def state_finish_creator():
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    keys = InlineKeyboardMarkup()
    keys.add(InlineKeyboardButton(text="Отмена", callback_data=state_finish_callback.new(finish='finish')))
    return keys

