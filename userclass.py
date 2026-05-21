import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash  # DÜZELTME: Güvenlik için eklendi

DB_PATH = Path(__file__).with_name('student_checking.db')


class User:
    def __init__(self, username, password, user_id):
        self.username = username
        self.password = password
        self.user_id = user_id

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    @staticmethod
    def register_user(username, password, user_id):
        conn = User.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ? OR username = ?', (user_id, username))
        if cursor.fetchone():
            conn.close()
            return False

        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)',
                       (user_id, username, hashed_password))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def login(username, password):
        conn = User.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            return user
        return None