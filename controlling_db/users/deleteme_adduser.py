import sqlite3
from controlling_db.users.user_model import User

db_file = "/Users/labiozzza/Desktop/Личные проекты/control_panel/controlling_db/users/users.db"
def add_user(user):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)', (
        user.telegram_id, user.username, user.first_name, user.last_name,
        user.language_code, user.is_premium, user.phone
    ))
    connection.commit()
    connection.close()

vasia = User(888, 'auto', 'Vasia', 'Petrov', 'ru', False, '79199485553')
add_user(vasia)
