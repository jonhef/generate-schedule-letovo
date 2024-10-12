import schedule
import icalendar
import datetime

class GenerateICS:
    def __init__(self):
        pass
    
    def generate(self, schedule: schedule.Schedule) -> bool:
        self.calendar = icalendar.Calendar()
        self.eatings = icalendar.Calendar()
        self.eatings.add("prodid", "https://github.com/jonhef/generate-schedule-letovo")
        self.eatings.add("version", "2.0")
        self.calendar.add("prodid", "https://github.com/jonhef/generate-schedule-letovo")
        self.calendar.add("version", "2.0")
        week = schedule.schedule
        for i in range(0, 7):
            for j in range(0, len(week[i].lessons)):
                e = icalendar.Event()
                e.name = "VEVENT"
                e.add("summary", week[i].lessons[j].name)
                e.add("dtstart", datetime.datetime(week[i].date.year, week[i].date.month, week[i].date.day) + datetime.timedelta(minutes=week[i].lessons[j].time_start.minute, hours=week[i].lessons[j].time_start.hour))
                e.add("dtend", datetime.datetime(week[i].date.year, week[i].date.month, week[i].date.day) + datetime.timedelta(minutes=week[i].lessons[j].time_end.minute, hours=week[i].lessons[j].time_end.hour))
                e.add("description", f"{week[i].lessons[j].room}")
                e.add("location", week[i].lessons[j].room)
                alarm = icalendar.Alarm()
                alarm.add("trigger;value=date-time", (datetime.datetime(week[i].date.year, week[i].date.month, week[i].date.day) + datetime.timedelta(minutes=week[i].lessons[j].time_start.minute-5, hours=week[i].lessons[j].time_start.hour-3)).strftime("%Y%m%dT%H%M%S") + "Z")
                alarm.add("action", "DISPLAY")
                alarm.add("description", f"{e.get('summary')} ({e.get('description')})")
                e.add_component(alarm)
                #e.alarms.append(ics.alarm.DisplayAlarm(week[i].lessons[j].time_start - datetime.timedelta(minutes=5), display_text=f"{e.name} ({e.description})"))
                if week[i].lessons[j].type == "eating":
                    self.eatings.add_component(e)
                else:
                    self.calendar.add_component(e)
        return True
    
    def save(self, path: str, path_eatings: str):
        with open(path, "w") as f:
            f.write(self.calendar.to_ical().decode())
        with open(path_eatings, "w") as f:
            f.write(self.eatings.to_ical().decode()) 