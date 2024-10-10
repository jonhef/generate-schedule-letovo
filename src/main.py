import calendargenerator
import get_schedule

if __name__ == "__main__":
    schedule = get_schedule.StudentLetovo("2027novozhilov.dm@student.letovo.ru", "KlW02!GSsRz")
    c = calendargenerator.GenerateICS()
    c.generate(schedule)
    c.save("test.ics")