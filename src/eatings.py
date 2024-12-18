import schedule

#monday
def get_eatings_monday(class_n: int, 
                       breakfast = True, 
                       lunch = True, 
                       snack = True, 
                       dinner = True, 
                       night_snack = True) -> "dict[str, schedule.Eating]":
    eating = {} 
    if breakfast: eating["breakfast"] = schedule.Eating({
        "type": "eating", 
        "name": "Завтрак", 
        "room": "Столовая", 
        "group_name": "", 
        "time_start": "7:40", 
        "time_end": "08:20"
    })
    if class_n in [7, 8, 10]:
        if lunch:eating["lunch"] = schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 7 or class_n == 8 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "11:45", 
            "time_end": "12:30"
        })
    else:
        if lunch: eating["lunch"] = schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 9 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "12:30", 
            "time_end": "13:20"
        })
    if snack: eating["snack"] = schedule.Eating({
        "type": "eating", 
        "name": "Полдник", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "15:35", 
        "time_end": "16:00"
    })
    if class_n == 10:
        if dinner: eating["dinner"] = schedule.Eating({
            "type": "eating", 
            "name": "Ужин", 
            "room": "Верхняя столовая", 
            "group_name": "", 
            "time_start": "19:25", 
            "time_end": "19:50"
        })
    else:
        if dinner: eating["dinner"] = schedule.Eating({
            "type": "eating", 
            "name": "Ужин", 
            "room": "Верхняя столовая", 
            "group_name": "", 
            "time_start": "18:10", 
            "time_end": "19:25"
        })
    if night_snack: eating["night_snack"] = schedule.Eating({
        "type": "eating",
        "name": "Сонник",
        "room": "",
        "group_name": "",
        "time_start": "20:20",
        "time_end": "20:50"
    })
    return eating
#tuesday-friday
def get_eatings_tuesday_friday(class_n: int,
                               breakfast = True, 
                               lunch = True, 
                               snack = True, 
                               dinner = True, 
                               night_snack = True) -> "dict[str, schedule.Eating]":
    eating = {}
    if breakfast: eating["breakfast"] = schedule.Eating({
        "type": "eating", 
        "name": "Завтрак", 
        "room": "Столовая", 
        "group_name": "", 
        "time_start": "7:40", 
        "time_end": "08:25"
    })
    if class_n in [7, 8, 10]:
        if lunch: eating["lunch"] = schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 7 or class_n == 8 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "11:40", 
            "time_end": "12:30"
        })
    else:
        if lunch: eating["lunch"] = schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 9 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "12:30", 
            "time_end": "13:20"
        })
    if snack: eating["snack"] = schedule.Eating({
        "type": "eating", 
        "name": "Полдник", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "15:35", 
        "time_end": "16:00"
    })
    if snack: eating["snack"] = schedule.Eating({
        "type": "eating", 
        "name": "Полдник", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "15:40", 
        "time_end": "16:10"
    })
    if dinner: eating["dinner"] = schedule.Eating({
        "type": "eating", 
        "name": "Ужин", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "18:25", 
        "time_end": "19:40"
    })
    if night_snack: eating["night_snack"] = schedule.Eating({
        "type": "eating",
        "name": "Сонник",
        "room": "",
        "group_name": "",
        "time_start": "20:20",
        "time_end": "20:50"
    })
    return eating
#saturday
def get_eatings_saturday(class_n: int, 
                         breakfast = True, 
                         lunch = True, 
                         snack = True, 
                         dinner = True, 
                         night_snack = True) -> "dict[str, schedule.Eating]":
    eating = {}
    if breakfast: eating["breakfast"] = schedule.Eating({
        "type": "eating", 
        "name": "Завтрак", 
        "room": "Столовая", 
        "group_name": "", 
        "time_start": "8:00", 
        "time_end": "09:00"
    })
    if class_n in [7, 8, 10]:
        if lunch: eating["lunch"] = schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 7 or class_n == 8 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "12:10", 
            "time_end": "13:00"
        })
    else:
        if lunch: eating["lunch"] = schedule.Eating({
            "type": "eating", 
            "name": "Обед", 
            "room": "Верхняя столовая" if class_n == 9 else "Нижняя столовая", 
            "group_name": "", 
            "time_start": "13:00", 
            "time_end": "13:50"
        })
    if snack: eating["snack"] = schedule.Eating({
        "type": "eating",
        "name": "Полдник",
        "room": "Верхняя столовая",
        "group_name": "",
        "time_start": "16:10",
        "time_end": "16:40"
    })
    if dinner: eating["dinner"] = schedule.Eating({
        "type": "eating",
        "name": "Ужин",
        "room": "Верхняя столовая",
        "group_name": "",
        "time_start": "18:20",
        "time_end": "19:10"
    })
    if night_snack: eating["night_snack"] = schedule.Eating({
        "type": "eating",
        "name": "Сонник",
        "room": "",
        "group_name": "",
        "time_start": "20:20",
        "time_end": "20:50"
    })
    return eating
#sunday
def get_eatings_sunday(class_n: int, 
                       breakfast = True, 
                       lunch = True, 
                       snack = True, 
                       dinner = True, 
                       night_snack = True) -> "dict[str, schedule.Eating]":
    eating = {}
    if breakfast: eating["breakfast"] = schedule.Eating({
        "type": "eating", 
        "name": "Завтрак", 
        "room": "Столовая", 
        "group_name": "", 
        "time_start": "9:00", 
        "time_end": "10:00"
    })
    if lunch: eating["lunch"] = schedule.Eating({
        "type": "eating", 
        "name": "Обед", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "12:15", 
        "time_end": "13:45"
    })
    if snack: eating["snack"] = schedule.Eating({
        "type": "eating", 
        "name": "Полдник", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "15:30", 
        "time_end": "16:00"
    })
    if dinner: eating["dinner"] = schedule.Eating({
        "type": "eating", 
        "name": "Ужин", 
        "room": "Верхняя столовая", 
        "group_name": "", 
        "time_start": "18:30", 
        "time_end": "19:30"
    })
    if night_snack: eating["night_snack"] = schedule.Eating({
        "type": "eating",
        "name": "Сонник",
        "room": "",
        "group_name": "",
        "time_start": "20:20",
        "time_end": "20:50"
    })
    return eating