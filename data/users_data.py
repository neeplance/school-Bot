from data import tests_path
from loader import db
import os

def users_sheet_creator(table_name):
    full_name = db.select_from('ФИО, chat_id', table_name)
    users_dict = {}
    for i in full_name:
        users_dict[i[1]]=i[0]
    return users_dict


students = users_sheet_creator('Ученики')
teachers = users_sheet_creator('Учителя')
organizators = users_sheet_creator('Организаторы')
users={'students':students, 'teachers':teachers, 'organizators':organizators}
disciplines = os.listdir(tests_path)

