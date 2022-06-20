from utils.db_api.sqlite import DataBase

db = DataBase()


def test():
    db.add_column(column_name='test', TableName="Математика")
    print(db.select_from_where(arg='FullName', value='FullName', table_name='Points'))
test()