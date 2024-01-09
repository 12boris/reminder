import sqlite3
from controlling_db.reminds.remind_model import Remind
import os

def initialize_db():
    # Получаем абсолютный путь к директории текущего файла (main.py)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Формируем путь к файлу базы данных
    db_path = os.path.join(current_directory, 'reminds.db')
    conn = sqlite3.connect(db_path)
    print(f"{db_path} инициализирован")
    return conn
conn = initialize_db()

def add_remind(conn, remind):
    with conn:
        conn.execute('INSERT INTO reminds (creator, task, remind_type, nearest_trigger) VALUES (?, ?, ?, ?)',
                     (remind.creator, remind.task, remind.remind_type, remind.nearest_trigger))

remind = Remind(777777, 'Встреча в 17:00', 'daily', 1672535500)
add_remind(conn, remind)