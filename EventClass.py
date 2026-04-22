import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name('student_checking.db')


class Event:
    def __init__(self, User_id, title, description, date, start_time, end_time, id=None):
        self.User_id = User_id
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    @staticmethod
    def add_event(user_id, id, title, description, date, start_time, end_time):
        conn = Event.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO events (id, user_id, title, description, date, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (id, user_id, title, description, date, start_time, end_time)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_events():
        conn = Event.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        conn.close()
        return events

    @staticmethod
    def get_event_with_user_id(User_id):
        conn = Event.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE user_id = ?', (User_id,))
        events = cursor.fetchall()
        conn.close()
        return events
