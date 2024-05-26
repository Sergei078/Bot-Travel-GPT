import logging
import sqlite3

from config import DB_FILE, user_token

path_to_db = DB_FILE  # файл базы данных


# создаём базу данных и таблицу messages
def create_database():
    try:
        # подключаемся к базе данных
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            # создаём таблицу messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_city (
                user_id INTEGER PRIMARY KEY,
                city TEXT,
                photo_id INTEGER,
                user_token INTEGER,
                translate TEXT)
            ''')
            logging.info("DATABASE: База данных создана")  # делаем запись в логах
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return None


def add_message(user_id):
    try:
        # подключаемся к базе данных
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            # записываем в таблицу новое сообщение
            cursor.execute('''
                    INSERT INTO user_city (user_id, city, photo_id, user_token, translate) 
                    VALUES (?, ?, ?, ?, ?)''',
                           (user_id, '', 0, user_token, '')
                           )
            conn.commit()  # сохраняем изменения
            logging.info(f"DATABASE: INSERT INTO messages "
                         f"well done!")
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return None


def select_city(user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT city
                FROM user_city
                WHERE user_id = ?
            ''', (user_id,))
            city = cursor.fetchone()[0]
            logging.info(f"DATABASE: Город пользователя {user_id} получен")
            return city
    except Exception as e:
        logging.error(e)


def select_token(user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_token
                FROM user_city
                WHERE user_id = ?
            ''', (user_id,))
            token = cursor.fetchone()[0]
            logging.info(f"DATABASE: Токен пользователя {user_id} получен")
            return token
    except Exception as e:
        logging.error(e)


def select_translate(user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT translate
                FROM user_city
                WHERE user_id = ?
            ''', (user_id,))
            token = cursor.fetchone()[0]
            logging.info(f"DATABASE: Токен пользователя {user_id} получен")
            return token
    except Exception as e:
        logging.error(e)


def update_translate(translate, user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_city
                SET translate = ?
                WHERE user_id = ?
            ''', (translate, user_id))
            conn.commit()
            logging.info(f"DATABASE: Город пользователя {user_id} обновлены")
    except Exception as e:
        logging.error(e)


def update_city(city, user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_city
                SET city = ?
                WHERE user_id = ?
            ''', (city, user_id))
            conn.commit()
            logging.info(f"DATABASE: Город пользователя {user_id} обновлены")
    except Exception as e:
        logging.error(e)


def update_token(user_id, token):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_city
                SET user_token = ?
                WHERE user_id = ?
            ''', (token, user_id))
            conn.commit()
            logging.info(f"DATABASE: Токены пользователя {user_id} обновлены")
    except Exception as e:
        logging.error(e)


def update_photo_id(user_id, photo_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_city
                SET photo_id = ?
                WHERE user_id = ?
            ''', (photo_id, user_id))
            conn.commit()
            logging.info(f"DATABASE: Фото пользователя {user_id} обновлены")
    except Exception as e:
        logging.error(e)
