from event import Event


class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        if not isinstance(event, Event):
            raise TypeError("Only Event objects can be added.")

        if self.get_event_by_id(event.event_id) is not None:
            raise ValueError("An event with this id already exists.")

        self.events.append(event)

    def get_event_by_id(self, event_id):
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None

    def remove_event(self, event_id):
        event = self.get_event_by_id(event_id)
        if event is None:
            return False

        self.events.remove(event)
        return True

    def get_events_by_date(self, day, month, year):
        matching_events = []

        for event in self.events:
            if event.day == day and event.month == month and event.year == year:
                matching_events.append(event)

        return matching_events

    def get_all_events(self):
        return sorted(
            self.events,
            key=lambda event: (event.year, event.month, event.day, event.start),
        )

    def update_event_description(self, event_id, description):
        event = self.get_event_by_id(event_id)
        if event is None:
            return False

        event.set_description(description)
        return True

    def update_event_time(self, event_id, start, end):
        event = self.get_event_by_id(event_id)
        if event is None:
            return False

        event.set_start(start)
        event.set_end(end)
        return True
