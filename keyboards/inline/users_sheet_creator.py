from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import files_in_folders

type_user_callback = CallbackData("type_user_callback", 'user_type')
user_callback_doc = CallbackData("user_callback_doc", "user_name")

choose_user_type = InlineKeyboardMarkup(row=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(
                                                  text="Ученики",
                                                  callback_data=type_user_callback.new(
                                                      user_type="students")
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text='Учителя',
                                                  callback_data=type_user_callback.new(
                                                      user_type='teachers')
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text='Организаторы',
                                                  callback_data=type_user_callback.new(
                                                      user_type='organizators')
                                              ),
                                          ],
                                      ])

def users_sheet_keyboard_doc(users_sheet, id, n=0):
    start_n = n
    users = InlineKeyboardMarkup()
    users_sheet = [a for a in users_sheet]
    users_sheet = users_sheet[n:]
    files_in_folders[id] = []

    for user in users_sheet:
        files_in_folders[id].append(user)
        users.add(InlineKeyboardButton(text=f'{user}', callback_data=user_callback_doc.new(user_name=f'{n}')))
        if n == start_n + 90:
            users.add(
                InlineKeyboardButton(text=f'Ещё', callback_data=user_callback_doc.new(user_name='more')))
            files_in_folders[f'{id}nn'] = n
            return users
        n += 1

    return users