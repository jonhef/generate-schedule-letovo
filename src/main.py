import calendargenerator
import schedule as _schedule
import datetime

if __name__ == "__main__":
    schedule = _schedule.StudentLetovo()
    schedule.login_student_letovo()
    schedule.get_me_student()
    schedule.get_schedule(datetime.datetime(2024, 10, 14))
    schedule.add_letovo_wednesday()
    schedule.add_summatives()
    schedule.add_eatings()
    schedule.add_assembly()
    schedule.add_house_meeting()
    generator = calendargenerator.GenerateICS()
    generator.generate(schedule, ["Междисциплинарное мышление", "Основы безопасности и защиты Родины", "Персональный проект"])
    generator.save("calendar.ics", "eatings.ics", "events.ics")