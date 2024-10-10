import calendargenerator
import get_schedule

if __name__ == "__main__":
    schedule = get_schedule.StudentLetovo()
    c = calendargenerator.GenerateICS()
    c.generate(schedule)
    c.save("test.ics")