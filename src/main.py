import calendargenerator
import schedule

if __name__ == "__main__":
    schedule = schedule.StudentLetovo()
    schedule.login_student_letovo()
    schedule.add_summatives()
    schedule.add_eatings()
    generator = calendargenerator.GenerateICS()
    generator.generate(schedule)
    generator.save("calendar.ics", "eatings.ics")