import sqlite3
from controlling_db.users.user_model import User
import os
import sys

db_file = "/Users/labiozzza/Desktop/Личные проекты/control_panel/controlling_db/users/users.db"

def init_users_db():
    if not os.path.exists(db_file):
        # Файл не существует, создаем его
        with open(db_file, "w") as file:
            print('created db_users_file')
    else:
        print('db_users_file_already_exists')
    create_users_table()

# Функция для создания таблицы "users", если она не существует
def create_users_table():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language_code TEXT,
            is_premium INTEGER,
            phone TEXT
        )
    ''')
    connection.commit()
    connection.close()
    print(f'table Users in {db_file} is exists')

# Функция для проверки существования пользователя по telegram_id
def user_exists(telegram_id):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()
    connection.close()
    return user is not None

# Функция для добавления пользователя
def add_user(user):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)', (
        user.telegram_id, user.username, user.first_name, user.last_name,
        user.language_code, user.is_premium, user.phone
    ))
    connection.commit()
    connection.close()

# Функция для удаления пользователя
def delete_user(telegram_id):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE telegram_id = ?', (telegram_id,))
    connection.commit()
    connection.close()


def get_all_users():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users_tuples = cursor.fetchall()
    connection.close()

    # Преобразование кортежей в объекты User
    users_objects = [
        User(telegram_id=t[0], username=t[1], first_name=t[2], last_name=t[3], language_code=t[4], is_premium=t[5],
             phone=t[6]) for t in users_tuples]

    return users_objects


init_users_db()
vasia = User(1121121, 'qqshka', 'Vasia', 'Petrov', 'ru', False, '79199485553')
#add_user(vasia)
#print(get_all_users())
#print(vasia.to_dict())
