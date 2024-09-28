import json
import locale
import datetime
import os

class Event:

    def __init__(self, title, date, time, location, description="", partners=None):
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        self.partners = partners

    def date_complete(self):
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        date_obj = datetime.datetime.strptime(self.date, "%d/%m/%Y")
        return date_obj.strftime("%A\n%d\n%B\n%Y")

    @staticmethod
    def str_date_to_date(date_str):
        return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
    
    @staticmethod
    def date_to_str_date(date):
        return date.strftime("%d/%m/%Y")

    @staticmethod
    def get_month_from_date(str_date):
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        date_obj = datetime.datetime.strptime(str_date, "%d/%m/%Y")
        return date_obj.strftime("%B")

    def get_month(self):
        return self.get_month_from_date(self.date)

    def get_week(self):
        date_obj = datetime.datetime.strptime(self.date, "%d/%m/%Y")
        return date_obj.isocalendar()[1]

    @staticmethod
    def load_events(file_path=None):

        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/events.json"

        with open(file_path, 'r') as file:
            events_data = json.load(file)
        return [Event(**event) for event in events_data]

    def save_event(self, file_path=None):

        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/events.json"

        try:
            with open(file_path, 'r') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            events_data = []
        
        events_data.append(self.__dict__)

        with open(file_path, 'w') as file:
            json.dump(events_data, file, indent=4)
    
    @staticmethod
    def sort_events_by_date(events):
        return sorted(events, key=lambda event: datetime.datetime.strptime(event.date, "%d/%m/%Y"))

    @staticmethod
    def get_events_from_month(month, file_path=None):
        
        events = Event.load_events(file_path)
        res = []
        
        for event in events:
            if event.get_month() == month:
                res.append(event)
        
        return Event.sort_events_by_date(res)
    
    @staticmethod
    def get_events_from_week(file_path=None):

        events = Event.load_events(file_path)

        events_by_week = {}
        
        for event in events:
            
            date_obj = datetime.datetime.strptime(event.date, "%d/%m/%Y")
            week_number = date_obj.isocalendar()[1]
            
            if week_number not in events_by_week:
                events_by_week[week_number] = []
            
            events_by_week[week_number].append(event)

        sorted_events = {}
        for week in events_by_week:
            sorted_events[week] = Event.sort_events_by_date(events_by_week[week])

        return sorted_events

    def __str__(self):
        return json.dumps(vars(self), indent=4)
