import calendargenerator
import schedule


if __name__ == "__main__":
    schedule = schedule.StudentLetovo()
    generator = calendargenerator.GenerateICS()
    generator.generate(schedule)
    generator.save("calendar.ics", "eatings.ics")