import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

events_callback = CallbackData("events_callback", "event")
events_org_callback = CallbackData("events_org_callback", "event", 'variant')
approve_callback = CallbackData('approve_callback', 'event')
add_to_event_callback = CallbackData('add_to_event_callback', 'student', 'event')


def events_creator(events):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    events_keyboard = InlineKeyboardMarkup()
    with open(events, 'r', encoding='utf-8') as f:
        events_data = json.load(f)
        f.close()

    for event in events_data:
        events_keyboard.add(InlineKeyboardButton(text=f'{event}', callback_data=events_callback.new(event=event)))
    return events_keyboard


def events_creator_org(events):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    events_keyboard = InlineKeyboardMarkup()
    with open(events, 'r', encoding='utf-8') as f:
        events_data = json.load(f)
        f.close()

    for event in events_data:
        print(1)
        events_keyboard.add(InlineKeyboardButton(text=f'{event}',
                                                 callback_data=events_org_callback.new(event=event, variant='choose')))
    events_keyboard.add(InlineKeyboardButton(text='Создать мероприятие',
                                             callback_data=events_org_callback.new(event='event', variant='create')))
    return events_keyboard


def event_info_or_add_st(event):
    events_keyboard = InlineKeyboardMarkup()
    events_keyboard.add(InlineKeyboardButton(text='Информация о мероприятии',
                                             callback_data=events_org_callback.new(event=event, variant='info')))
    events_keyboard.add(InlineKeyboardButton(text='Добавить участника',
                                             callback_data=events_org_callback.new(event=event, variant='add st')))
    return events_keyboard


def approve(event_name):
    # Возвращает клавиатуру, построенную на основе файлов в директории, в которой находится программа
    approve_keyboard = InlineKeyboardMarkup()

    approve_keyboard.add(InlineKeyboardButton(text=f'Записаться', callback_data=approve_callback.new(event=event_name)))
    approve_keyboard.add(
        InlineKeyboardButton(text=f'Записать команду', callback_data=add_to_event_callback.new(student='team',
                                                                                                        event=event_name)))
    approve_keyboard.add(InlineKeyboardButton(text=f'Посмотреть другие мероприятия',
                                              callback_data=events_callback.new(event=0)))
    return approve_keyboard


def add_to_event(students_sheet, event, id, n=0):
    start_n = n
    keyboard = InlineKeyboardMarkup()
    students_sheet = [n for n in students_sheet]
    students_sheet = students_sheet[n:]
    files_in_folders[id] = []
    keyboard.add(InlineKeyboardButton(text=f'Добавить команду', callback_data=add_to_event_callback.new(student='team',
                                                                                                        event=event)))
    for student in students_sheet:
        files_in_folders[id].append(student)
        keyboard.add(InlineKeyboardButton(text=f'{student}', callback_data=add_to_event_callback.new(student=n,
                                                                                                     event=event)))
        if n == start_n + 90:
            keyboard.add(
                InlineKeyboardButton(text=f'Ещё', callback_data=add_to_event_callback.new(student=n, event='more')))
            files_in_folders[f'{id}nn'] = n
            return keyboard
        n += 1


    files_in_folders[id].append(event)
    return keyboard
