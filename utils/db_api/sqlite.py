import sqlite3
from data.config import db_path

class DataBase:
    def __init__(self, path_to_db=db_path):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):

        if not parameters:
            parameters = tuple()

        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_students(self):
        sql = """
        CREATE TABLE Students (
        chat_id int NOT NULL,
        Nickname varchar(255) NOT NULL,
        FullName varchar(255) NOT NULL,
        PhoneNumber varchar(255) NOT NULL,
        GroupType varchar(255) NOT NULL,
        VozhNickname verchar(255) NOT NULL,
        NumberOfPoints int,
        Rate,
        PRIMARY KEY (chat_id)
        );
        """
        self.execute(sql, commit=True)

    def create_table_rate(self):
        sql = """
        CREATE TABLE Математика (
        chat_id int NOT NULL,
        FullName varchar(255) NOT NULL,
        SUMM int NOT NULL,
        PRIMARY KEY (SUMM)
        );
        """
        self.execute(sql, commit=True)

    def create_table_teachers(self):
        sql = """
        CREATE TABLE Teachers (
        chat_id int NOT NULL,
        Nickname varchar(255) NOT NULL,
        FullName varchar(255) NOT NULL,
        PhoneNumber varchar(255) NOT NULL,
        PRIMARY KEY (chat_id)
        );
        """
        self.execute(sql, commit=True)

    def create_table_organizators(self):
        sql = """
        CREATE TABLE Organizators (
        chat_id int NOT NULL,
        Nickname varchar(255) NOT NULL,
        FullName varchar(255) NOT NULL,
        PhoneNumber varchar(255) NOT NULL,
        PRIMARY KEY (chat_id)
        );
        """
        self.execute(sql, commit=True)

    def put_a_rating(self, FullName, task, rate, TableName):
        sql = f"UPDATE {TableName} SET {task}=? WHERE ФИО=?"
        return self.execute(sql, parameters=(rate, FullName), commit=True)

    def put_a_rating_auto(self, TableName, chat_id, task, rate):
        sql = f"UPDATE {TableName} SET {task}=? WHERE chat_id=?"
        return self.execute(sql, parameters=(rate, chat_id), commit=True)

    def insert_into_table(self, TableName, columns, values):
        sql = f"INSERT INTO '{TableName}'({columns})\n" \
              f"VALUES({('?, '*len(values))[:-2]})"
        print(sql)
        self.execute(sql, parameters=values, commit=True)

    def add_student(self, kwargs):
        sql = "INSERT INTO Students (chat_id, Nickname, ФИО, Номер_телефона, Группа, Вожатый) " \
              "VALUES({?, ?, ?, ?, ?, ?})"
        parameters = (kwargs)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all(self, TableName):
        sql = f"SELECT * FROM {TableName}"
        return self.execute(sql, fetchall=True)


    def return_columns(self, TableName):
        sql = f"PRAGMA table_info({TableName})"
        return self.execute(sql, fetchall=True)


    def select_from(self, arg, table_name):
        sql = f"SELECT {arg} FROM {table_name}"
        return self.execute(sql, fetchall=True)

    def select_from_where(self, table_name, arg, value):
        sql = f"SELECT * FROM {table_name} WHERE {arg}='{value}'"
        return self.execute(sql, fetchall=True)


    def select_one_from_where(self, column, table_name, arg, value):
        sql = f"SELECT {column} FROM {table_name} WHERE {arg}='{value}'"
        return self.execute(sql, fetchone=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_student(self, **kwargs):

        sql = "SELECT * FROM Ученики WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self. execute(sql, parameters, fetchone=True)

    def count_students(self):
        self.execute("SELECT COUNT(*) FROM Students;")

    def update(self, TableName, data, FullName):
        sql = f"UPDATE {TableName} SET Баллов_итого=Баллов_итого+? WHERE ФИО=?"
        return self.execute(sql, parameters=(data, FullName), commit=True)


    def update_summ(self, data, FullName, TableName):
        sql = f"UPDATE {TableName} SET SUMM=SUMM+{data} WHERE ФИО={FullName}"
        print(sql)
        return self.execute(sql, commit=True)

    def add_column(self, column_name, TableName):
        sql = f"ALTER TABLE {TableName} ADD COLUMN {column_name}"
        print(sql)
        return self.execute(sql, commit=True)


    def delete_users(self):
        self.execute("DELETE FROM Users WHERE True")



def logger(statement):
    print(f"""
__________________________________________________________________
Executing:
{statement}
__________________________________________________________________
""")
