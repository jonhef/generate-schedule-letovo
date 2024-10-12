import calendargenerator
import schedule
import events
import datetime

if __name__ == "__main__":
    schedule = schedule.StudentLetovo()
    schedule.login_student_letovo()
    schedule.get_schedule(datetime.datetime(2024, 10, 14))
    events.add_letovo_wednesday(schedule)
    schedule.add_summatives()
    schedule.add_eatings()
    generator = calendargenerator.GenerateICS()
    generator.generate(schedule, ["Междисциплинарное мышление", "Основы безопасности и защиты Родины", "Персональный проект"])
    generator.save("calendar.ics", "eatings.ics", "events.ics")