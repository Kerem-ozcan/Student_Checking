class Event:
    def __init__(self, day, month, year, event_id, description, start, end):
        self.day = day
        self.month = month
        self.year = year
        self.event_id = event_id
        self.description = description
        self.start = start
        self.end = end

    def set_day(self, day):
        self.day = day

    def set_month(self, month):
        self.month = month

    def set_year(self, year):
        self.year = year

    def set_event_id(self, event_id):
        self.event_id = event_id

    def set_description(self, description):
        self.description = description

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end



