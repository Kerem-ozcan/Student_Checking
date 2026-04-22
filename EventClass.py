import sqlite3


class Event:
    def __init__(self, User_id,title, description, date, start_time, end_time, id=None):
        self.User_id = User_id 
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
    def add_event(user_id, id, title, description, date, start_time, end_time):
        conn = Event.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (id, title, description, date, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?)',
                      (user_id, id, title, description, date, start_time, end_time))
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
        cursor.execute('SELECT * FROM events WHERE user_id = ?', (user_id,))
        events = cursor.fetchall()
        conn.close()
        return events