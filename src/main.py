import calendargenerator
import schedule

if __name__ == "__main__":
    schedule = schedule.StudentLetovo("2027novozhilov.dm@student.letovo.ru", "KlW02!GSsRz")
    schedule.login_student_letovo()
    schedule.add_summatives()
    schedule.add_eatings()
    generator = calendargenerator.GenerateICS()
    generator.generate(schedule)
    generator.save("calendar1.ics", "eatings1.ics")