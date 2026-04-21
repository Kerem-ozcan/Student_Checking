import sqlite3


class User:
    def __init__(self, username, password, user_id):
        self.username = username
        self.password = password
        self.user_id = user_id

    @staticmethod
    def get_db_connection():
        return sqlite3.connect('student_checking.db')

    @staticmethod
    def register_user(username, password, user_id):
        conn = User.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        if cursor.fetchone():
            conn.close()
            return False
        cursor.execute('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)',
                      (user_id, username, password))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def login(username, password):
        conn = User.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

