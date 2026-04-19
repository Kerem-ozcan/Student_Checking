import json


class Event:
    def __init__(self, title , description , date , start_time, end_time):
        self.title = title
        self.description = description
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    def add_event(self,title,description,date,start_time,end_time):
        with open("event_data.json", "r") as read_file:
            data = json.load(read_file)
            new_event = Event(title,description,date,start_time,end_time).to_dict()

        data["events"].append(new_event)

        with open("event_data.json", "w") as write_file:
            json.dump(data, write_file, indent=4)
