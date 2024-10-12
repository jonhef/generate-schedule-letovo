import schedule

class Event(schedule.Task):
    pass

def add_letovo_wednesday(schedule: schedule.Schedule):
    schedule.schedule[2].lessons.append(Event({
        "type": "event",
        "name": "Летовская среда",
        "room": "Зимний сад",
        "group_name": "",
        "time_start": "19:20",
        "time_end": "20:30"
    }))
    schedule.schedule[2].sort()

def add_event(schedule: schedule.Schedule, name: str, room: str, time_start: str, time_end: str, weekday: int):
    """schedule - your schedule where you want to add the event
    room - room where the event will be
    time_start - time when the event will start(in format %H:%M)
    time_end - time when the event will end(in format %H:%M)
    weekday - day of the week(0 - Monday to 6 - Sunday)"""
    schedule.schedule[weekday].lessons.append(Event({
        "type": "event",
        "name": name,
        "room": room,
        "group_name": "",
        "time_start": time_start,
        "time_end": time_end
    }))
    schedule.schedule[weekday].sort()