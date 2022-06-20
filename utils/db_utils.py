import os

import pandas as pd

from data import solve_path, students_doc_path, teachers_doc_path
from data.users_data import disciplines
from loader import db


async def columns_names(TableName):
    table = db.return_columns(TableName)
    column_names = [n[1] for n in table]
    return column_names


async def rate_checker(FullName, task_name, TableName):
    # Проверяет выставлена ли за задачу оценка
    rate = db.select_one_from_where(column=task_name, table_name=TableName, arg='ФИО', value=FullName)[0]
    print(rate)
    if rate == 'Null' or rate == None:
        return False
    return True


async def return_rate(FullName, TableName):
    # Возвращает оформленную успеваемость пользователя, пропуская те задачи, где у него не стоит оценка
    columns = await columns_names(TableName)

    rates = db.select_from_where(table_name=TableName, arg='ФИО', value=FullName)[0]

    rates_str = f'{rates[1]}'
    for n in range(3, len(rates)):
        if rates[n] == None or rates[n] == 'None' or int(rates[n]) == 0:
            continue
        else:
            rates_str += f'\n{columns[n]}: {rates[n]}'

    rates_str += f'\nИтого: {rates[2]}'

    return rates_str


async def save_data_to_excel(TableName, path_to_save):
    # Сохраняет данные из SQL таблицы в excel
    columns = await columns_names(TableName)

    data2 = {}
    data1 = db.select_from(arg="*", table_name=TableName)

    for a in range(0, len(columns)):
        for b in range(0, len(data1)):
            try:
                data2[columns[a]].append(data1[b][a])
            except:
                data2[columns[a]] = []
                data2[columns[a]].append(data1[b][a])

    df = pd.DataFrame(data2)
    save_path = rf'{path_to_save}\{TableName}.xlsx'
    df.to_excel(save_path, sheet_name='Страница 1', index=False)
    return save_path


async def add_users(document, TableName):
    # Загружает в таблицу 'TableName' значения из эксель файла 'document'
    columns = await columns_names(TableName)
    data_file = pd.read_excel(document)
    data_file = data_file.dropna(subset=['chat_id'])
    column_data = []

    hard_data = []
    for column in columns:
        column_data.append(data_file[column].values)

    for a in range(len(column_data[0])):
        hard_data.append([])
        for b in range(0, len(column_data)):
            hard_data[a].append(column_data[b][a])

    for i in range(0, len(columns)):
        try:
            db.insert_into_table(TableName=TableName, columns=(', '.join(columns)), values=tuple(hard_data[i]))
            if TableName == 'Ученики':
                os.mkdir(rf'{solve_path}\{hard_data[i][1]}')
                os.mkdir(rf'{students_doc_path}\{hard_data[i][1]}')
                for table in disciplines:
                    db.insert_into_table(TableName=table, columns=(', '.join(columns[:2])), values=tuple(hard_data[i][:2]))
            if TableName == 'Учителя':
                os.mkdir(rf'{teachers_doc_path}\{hard_data[i][1]}')
        except:
            pass


