import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('student_checking.db')


class Event:
    def __init__(self, user_id, title, description, date, start_time, end_time, id=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def get_event_type(self):
        return "General Event"

    def get_details(self):
        return (
            f"{self.get_event_type()}: {self.title} on {self.date} "
            f"from {self.start_time} to {self.end_time}"
        )

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    @staticmethod
    def add_event(user_id, title, description, date, start_time, end_time):
        conn = Event.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO events (user_id, title, description, date, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, title, description, date, start_time, end_time)
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


class ExamEvent(Event):
    def __init__(self, User_id, title, description, date, start_time, end_time, course_name, id=None):
        super().__init__(User_id, title, description, date, start_time, end_time, id)
        self.course_name = course_name

    def get_event_type(self):
        return "Exam Event"

    def get_details(self):
        return f"{super().get_details()} for course: {self.course_name}"


class MeetingEvent(Event):
    def __init__(self, User_id, title, description, date, start_time, end_time, location, id=None):
        super().__init__(User_id, title, description, date, start_time, end_time, id)
        self.location = location

    def get_event_type(self):
        return "Meeting Event"

    def get_details(self):
        return f"{super().get_details()} at location: {self.location}"