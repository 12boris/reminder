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

# Создание таблицы напоминаний
def create_table_if_not_exists(conn=initialize_db()):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reminds (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            creator TEXT NOT NULL,
                            task TEXT NOT NULL,
                            remind_type TEXT NOT NULL,
                            nearest_trigger INTEGER NOT NULL
                        );''')
        print("Таблица создана (если не существовала)")
        conn.close()
create_table_if_not_exists()

# Добавление напоминания в базу данных
def add_remind(remind,conn=initialize_db()):
    try:
        with conn:
            conn.execute('INSERT INTO reminds (creator, task, remind_type, nearest_trigger) VALUES (?, ?, ?, ?)',
                         (remind.creator, remind.task, remind.remind_type, remind.nearest_trigger))
    finally:
        conn.close()

# remind = Remind(123451234123226, 'Встреча в 17:00', 'ежедневные', 1672531200)
# add_remind(conn, remind)

# Получение всех напоминаний из базы данных. Если добавить telegram_id в аргемент, то выдаст  только этого пользователя
def get_all_reminds(telegram_id=None):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_directory, 'reminds.db')
    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()
        query = 'SELECT * FROM reminds'
        params = ()

        if telegram_id is not None:
            query += ' WHERE creator = ?'
            params = (telegram_id,)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            print("Напоминаний в базе данных не найдено.")
            return []

        reminders = []
        for row in rows:
            reminder = Remind(row[1], row[2], row[3], row[4])
            reminder.id = row[0]  # Установка ID внутри цикла
            reminders.append(reminder.__dict__)

        return reminders
    finally:
        conn.close()




if __name__ == "__main__":
    create_table_if_not_exists()
    # Пример вызова функции для проверки
    get_all_reminds()


# all_reminders = get_all_reminds(conn, 123456)
# for r in all_reminders:
#     print(r.to_json())

