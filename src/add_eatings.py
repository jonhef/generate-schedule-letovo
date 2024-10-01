import get_schedule

#monday
def get_eatings_monday(class_n: int) -> "dict[str, get_schedule.Eating]":
    eating = {}
    eating["breakfast"] = get_schedule.Eating({
        "type": "eating", 
        "name": "Завтрак", 
        "room": "Столовая", 
        "group_name": "", 
        "time_start": "7:40", 
        "time_end": "08:20"
    })
    if class_n in [7, 8, 10]:
        eating["lunch"] = get_schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 7 or class_n == 8 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "11:45", 
            "time_end": "12:30"
        })
    else:
        eating["lunch"] = get_schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 9 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "12:30", 
            "time_end": "13:20"
        })
    eating["snack"] = get_schedule.Eating({
        "type": "eating", 
        "name": "snack", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "15:35", 
        "time_end": "16:00"
    })
    if class_n == 10:
        eating["dinner"] = get_schedule.Eating({
            "type": "eating", 
            "name": "dinner", 
            "room": "Верхняя столовая", 
            "group_name": "", 
            "time_start": "19:25", 
            "time_end": "19:50"
        })
    else:
        eating["dinner"] = get_schedule.Eating({
            "type": "eating", 
            "name": "dinner", 
            "room": "Верхняя столовая", 
            "group_name": "", 
            "time_start": "18:10", 
            "time_end": "19:25"
        })
#tuesday-friday
def get_eatings_tuesday_friday(class_n: int) -> "dict[str, get_schedule.Eating]":
    eating = {}
    eating["breakfast"] = get_schedule.Eating({
        "type": "eating", 
        "name": "Завтрак", 
        "room": "Столовая", 
        "group_name": "", 
        "time_start": "7:40", 
        "time_end": "08:25"
    })
    if class_n in [7, 8, 10]:
        eating["lunch"] = get_schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 7 or class_n == 8 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "11:45", 
            "time_end": "12:30"
        })
    else:
        eating["lunch"] = get_schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 9 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "12:30", 
            "time_end": "13:20"
        })
    eating["snack"] = get_schedule.Eating({
        "type": "eating", 
        "name": "snack", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "15:35", 
        "time_end": "16:00"
    })
    eating["snack"] = get_schedule.Eating({
        "type": "eating", 
        "name": "snack", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "15:30", 
        "time_end": "16:00"
    })
    eating["dinner"] = get_schedule.Eating({
        "type": "eating", 
        "name": "dinner", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "18:15", 
        "time_end": "19:30"
    })
#saturday
def get_eatings_saturday(class_n: int) -> "dict[str, get_schedule.Eating]":
    eating = {}
    eating["breakfast"] = get_schedule.Eating({
        "type": "eating", 
        "name": "Завтрак", 
        "room": "Столовая", 
        "group_name": "", 
        "time_start": "8:00", 
        "time_end": "09:00"
    })
    if class_n in [7, 8, 10]:
        eating["lunch"] = get_schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 7 or class_n == 8 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "12:10", 
            "time_end": "13:00"
        })
    else:
        eating["lunch"] = get_schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 9 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "13:00", 
            "time_end": "13:50"
        })
    eating["snack"] = get_schedule.Eating({
        "type": "eating",
        "name": "snack",
        "room": "Верхняя столовая",
        "group_name": "",
        "time_start": "16:10",
        "time_end": "16:40"
    })
    eating["dinner"] = get_schedule.Eating({
        "type": "eating",
        "name": "dinner",
        "room": "Верхняя столовая",
        "group_name": "",
        "time_start": "18:20",
        "time_end": "19:10"
    })
    eating["night_snack"] = get_schedule.Eating({
        "type": "eating",
        "name": "night_snack",
        "room": ""
    })