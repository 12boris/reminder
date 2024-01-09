from flask import Flask, render_template
from flask import jsonify


from controlling_db.users.main import get_all_users
from controlling_db.users.user_model import User
from controlling_db.reminds.main import get_all_reminds

import logging
from logging.handlers import RotatingFileHandler

from flask_caching import Cache


app = Flask(__name__)
# Настройки логирования
def setup_logging():
    # Создайте обработчик, который пишет сообщения логов в файл
    # 'maxBytes=10000' означает, что файл будет "перекатываться" после достижения 10КБ
    # 'backupCount=3' означает, что будет храниться до трех файлов журнала резервных копий
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)

    # Установите уровень логирования
    handler.setLevel(logging.INFO)

    # Создайте формат логирования
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Добавьте обработчик к логгеру Flask
    app.logger.addHandler(handler)


# Вызовите эту функцию до запуска приложения
setup_logging()



# Конфигурация кэширования
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def index():
    users = get_all_users()
    app.logger.info('Index page is accessed')
    return render_template('index.html', users=users)


@app.route('/get-users')
@cache.cached(timeout=15)  # кэш сохраняется в течение 50 секунд
def get_users():
    """
        Ендпоинт, запрашивающий и принимающий всех пользователей в формате JSON
    """
    try:
        users = get_all_users()
        return jsonify(users=[user.to_dict() for user in users])
    except Exception as e:
        app.logger.error(f"Error retrieving users: {e}")
        return jsonify(error=str(e)), 500  # Возвращает код состояния HTTP 500


@app.route('/reminders')
def reminders():
    return render_template('reminds.html')

@app.route('/get-reminders')
@cache.cached(timeout=15)  # кэш сохраняется в течение 50 секунд
def get_reminders():
    """
    Ендпоинт, запрашивающий и принимающий все напоминнаия в формате JSON
    """
    try:
        reminders = get_all_reminds()
        return jsonify(reminders=reminders)
    except Exception as e:
        app.logger.error(f"Error retrieving reminders: {e}")
        return jsonify(error=str(e)), 500



if __name__ == '__main__':
    app.run(debug=True)
