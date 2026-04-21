import sqlite3


class Event:
    def __init__(self, title, description, date, start_time, end_time, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
    def get_db_connection():
        return sqlite3.connect('student_checking.db')

    @staticmethod
    def add_event(title, description, date, start_time, end_time):
        conn = Event.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (title, description, date, start_time, end_time) VALUES (?, ?, ?, ?, ?)',
                      (title, description, date, start_time, end_time))
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
