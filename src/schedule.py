import requests
import logging
import datetime
import eatings as eating
import json
import re
import regex
import bs4

def add_letovo_wednesday(schedule: "Schedule"):
    schedule.schedule[2].lessons.append(Event({
        "type": "event",
        "name": "Летовская среда",
        "room": "Зимний сад",
        "group_name": "",
        "time_start": "19:20",
        "time_end": "20:30"
    }))
    schedule.schedule[2].sort()

def add_event(schedule: "Schedule", name: str, room: str, time_start: str, time_end: str, weekday: int):
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
    
class Week:
    def __init__(self, week: "list[Day]", date: datetime.datetime) -> None:
        self._week = week
        if len(week) < 8:
            self._week.extend([None] * (8 - len(week)))
        self._date = date
        
    def __getitem__(self, key: int) -> "Day":
        return self._week[key]
    
    def __setitem__(self, key: int, value: "Day"):
        self._week[key] = value

class Day:
    def __init__(self, days: "list[Lesson]", date: datetime.datetime) -> None:
        self._days = days
        self._date = date    
        
    @property
    def date(self) -> datetime.datetime:
        return self._date
    
    @property
    def weekday(self) -> int:
        return self._date.weekday()
        
    @property
    def lessons(self) -> "list[Lesson]":
        return self._days
    
    def sort(self):
        self._days.sort()
        
    def add(self, task: "Task"):
        self.lessons.append(task)
        self.sort()
        
class Task:
    def __init__(self, task: dict):
        self.type = task["type"]
        self.name = task["name"]
        self.room = task["room"]
        self.group_name = task["group_name"]
        self.time_start = datetime.datetime.strptime(task["time_start"], "%H:%M")
        self.time_end = datetime.datetime.strptime(task["time_end"], "%H:%M")
        self.description = task.get("description")
        
    def __cmp__(self, other):
        if self.time_start < other.time_start:
            return -1
        if self.time_start > other.time_start:
            return 1
        return 0
    
    def __lt__(self, other):
        return self.time_start < other.time_start
    
    def __le__(self, other):
        return self.time_start <= other.time_start
    
    def __gt__(self, other):
        return self.time_start > other.time_start
    
    def __ge__(self, other):
        return self.time_start >= other.time_start
    
    def time(self) -> int:
        return self.time_start.hour * 60 * 60 + self.time_start.minute * 60 + self.time_start.second
    
class Event(Task):
    pass

class HomeWork(Task):
    def __init__(self, homework: dict):
        super().__init__(homework)
        
    def __str__(self) -> str:
        return f"{self.name} ({self.room})"
    
    def __cmp__(self, other):
        return super().__cmp__(other)
    
class Eating(Task):
    def __init__(self, eating: dict):
        super().__init__(eating)
        
    def __str__(self) -> str:
        return f"{self.name} ({self.room})"
    
    def __cmp__(self, other):
        return super().__cmp__(other)

class Lesson(Task):
    def __init__(self, lesson: dict):
        super().__init__(lesson)
        
    def __str__(self) -> str:
        return f"{self.name} ({self.room})"

    def __cmp__(self, other):
        return super().__cmp__(other)

#нужен класс, наследованный от этого
class Schedule:
    def __init__(self):
        self.schedule: Week = None
        
    def get_schedule(self, first_day: datetime.datetime = None) -> "Week":
        today = datetime.datetime.today() if first_day is None else first_day
        weekday = today.weekday()
        if weekday == 6:
            today = today + datetime.timedelta(days=1)
        if weekday != 0:
            today = today - datetime.timedelta(days=weekday)
        res = Week([], today)
        for i in range(0, 7):
            req = self.session.get(f"https://elk.letovo.ru/api/education_track/schedule?date={today.year}-{today.month}-{today.day}")
            if req.status_code != 200:
                logging.error("Failed to get schedule")
                res.append([])
                continue    
            obj = req.json()
            temp = []
            for j in obj:
                if j["type"] == "lesson":
                    temp.append(Lesson(j))
            res[i] = Day(temp, today)
            today = today + datetime.timedelta(days=1)
        # self.table = res
        self.schedule = res
        return res

class StudentLetovo(Schedule):
    def get_schedule(self, first_day: datetime.datetime = None) -> Week:
        res = super().get_schedule(first_day)
        self.get_teachers()
        if self.got_teachers:
            for i in range(0,7):
                for l in res[i].lessons:
                    l.description = self.teachers_dict[l.name]["teacher"]
        return res
    
    def _request_post(self, url: str, headers: dict = None, cookies: dict = None, data: dict | str = None):
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        if data is None:
            pass
        headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
        return self.session.post(url, data = data, headers = headers, cookies = cookies, verify=False)
    
    def add_letovo_wednesday(self):
        add_letovo_wednesday(self)
    
    def _request_get(self, url: str, headers: dict = None, cookies: dict = None):
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
        return self.session.get(url, headers = headers, cookies = cookies, verify=False)
        
    def _request_student_html(self, url):
        return self._request_get(url, {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
        }, cookies = {
            "PHPSESSID": self.student_phpsessid,
            "X-Csrf-Token": self.student_csrf
        })
        
    def add_reminder_create_schedule(self):
        add_event(self, "Создать расписание на неделю", "", "21:00", "21:15", 6)     
        
    def add_house_meeting(self):
        if self.student_me["Boarding"]["type"] == "Полный" or self.student_me["Boarding"]["type"] == "Недельный":
            add_event(self, "House meeting", "Common room", "21:15", "21:30", 0)
    
    def get_me_student(self):
        self._student_letovo_home()
        req = self._request_student_html("https://student.letovo.ru/student/1")
        res = {}
        res["Boarding"] = {"type": re.compile(r"<div class=\"col-sm-12 col-md-4 font-weight-bold\">Пансион</div>\s+<div class=\"col-sm-12 col-md-8\">\s+<span class=\"badge badge-info\">\s+([А-Яа-я]+)\s+</span>").findall(req.text)[0]}
        res["FIO"] = re.compile(r"<div class=\"col-sm-12 col-md-4 font-weight-bold\">ФИО</div>\s+<div class=\"col-sm-12 col-md-8\">([А-Яа-я ]+)</div>").findall(req.text)[0]
        res["Class"] = int(re.compile(r"<div class=\"row mb-1\">\s+<div class=\"col-sm-12 col-md-4 font-weight-bold\">Класс</div>\s+<div class=\"col-sm-12 col-md-8\">(\d+)</div>").findall(req.text)[0])
        res["Login"] = re.compile(r"<div class=\"row mb-1\">\s+<div class=\"col-sm-12 col-md-4 font-weight-bold\">Логин</div>\s+<div class=\"col-sm-12 col-md-8\">([A-Za-z0-9.@]+)</div>\s+</div>").findall(req.text)[0]
        res["Email"] = re.compile(r"<div class=\"row mb-1\">\s+<div class=\"col-sm-12 col-md-4 font-weight-bold\">Школьная почта</div>\s+<div class=\"col-sm-12 col-md-8\">([A-Za-z.@0-9]+)</div>\s+</div>").findall(req.text)[0]
        res["RealEmail"] = re.compile(r"<div class=\"row mb-1\">\s+<div class=\"col-sm-12 col-md-4 font-weight-bold\">Личная почта</div>\s+<div class=\"col-sm-12 col-md-8\">\s+(.+)\s+</div>\s+</div>").findall(req.text)[0]
        res["Number"] = re.compile(r"<div class=\"row mb-1\">\s+<div class=\"col-sm-12 col-md-4 font-weight-bold\">Мобильный номер</div>\s+<div class=\"col-sm-12 col-md-8\">\s+(.+)\s+</div>\s+</div>").findall(req.text)[0]
        res["Boarding"]["house"] = re.compile(r"<br\/><span style=\"display: inline-block; width: 80px;\">Дом: <\/span>\s+<b>House (\d+)<\/b>\s+<br\/>").findall(req.text)[0]
        res["Boarding"]["dorm"] = re.compile(r"<span style=\"display: inline-block; width: 80px;\">Комната: </span>\s+<b>Dorm (\d+)</b>").findall(req.text)[0]
        
        for k in res:
            if res[k] == "<i>нет доступа</i>":
                res[k] = None
                
        self.student_me = res
        return res

    def add_eatings(self):
        type_of_boarding = 2 if self.student_me["Boarding"]["type"] == "Полный" else (1 if self.student_me["Boarding"]["type"] == "Недельный" else 0)
        if type_of_boarding == 2:
            monday = eating.get_eatings_monday(self.class_n)
            tuesday_friday = eating.get_eatings_tuesday_friday(self.class_n)
            saturday = eating.get_eatings_saturday(self.class_n)
            sunday = eating.get_eatings_sunday(self.class_n)
        elif type_of_boarding == 1:
            monday = eating.get_eatings_monday(self.class_n)
            tuesday_friday = eating.get_eatings_tuesday_friday(self.class_n)
            saturday = eating.get_eatings_saturday(self.class_n, night_snack = False)
            sunday = {}
        elif type_of_boarding == 0:
            monday = eating.get_eatings_monday(self.class_n, dinner = False, night_snack=False)
            tuesday_friday = eating.get_eatings_tuesday_friday(self.class_n, dinner = False, night_snack = False)
            saturday = eating.get_eatings_saturday(self.class_n, dinner = False, night_snack = False)
            sunday = {}
            
        for k, v in monday.items():
                self.schedule[0].lessons.append(v)
        for k, v in tuesday_friday.items():
            for i in range(1, 5):
                self.schedule[i].lessons.append(v)
        for k, v in saturday.items():
            self.schedule[5].lessons.append(v)
        for k, v in sunday.items():
            self.schedule[6].lessons.append(v)
        for i in range(0, 7):
            self.schedule[i].sort()
            
    def add_assembly(self):
        if self.class_n == 7:
            add_event(self, "Ассамблея", "Жёлтые диваны", "9:05", "9:25", 0)
        elif self.class_n == 8:
            add_event(self, "Ассамблея", "Малый спортиный зал", "9:05", "9:25", 0)
        elif self.class_n == 9:
            add_event(self, "Ассамблея", "Большой спортиный зал", "9:05", "9:25", 0)
        elif self.class_n == 10:
            add_event(self, "Ассамблея", "Лекторий", "9:05", "9:25", 0)
        elif self.class_n == 11:
            add_event(self, "Ассамблея", "Тихий зал", "9:05", "9:25", 0)
    
    def login_student_letovo(self, login: str = None, password: str = None):
        self.student_login = login
        self.student_password = password
        if login is None:
            self.student_login = self.email.split('@')[0]
        if password is None:
            self.student_password = self.password
        verify = False # Set to False when using a proxy

        r_csrf = self._request_get("https://student.letovo.ru/login")
        cookies = r_csrf.headers.get("Set-Cookie")
        if not self.student_phpsessid and cookies is not None:
            phpsessid = regex.search("(?<=PHPSESSID=)[a-zA-Z0-9]+", cookies).group(0)
        phpsessid = self.student_phpsessid
        csrf = regex.search("(?<=_token( )*:( )*')[a-zA-Z0-9]+", r_csrf.text).group(0)
        # print("CSRF: " + csrf)
        # username = input("username: ")
        # password = input("password: ")
        username = self.student_login
        password = self.student_password
        self.student_phpsessid = phpsessid
        self.student_csrf = csrf
        r_login = self._request_post("https://student.letovo.ru/login", data=f"_token={csrf}&login={username}&password={password}", headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Csrf-Token": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
        })
        self._student_letovo_home()
        return r_login

        # print("PHPSESSID: " + phpsessid)

    def _student_letovo_home(self):
        return self._request_student_html("https://student.letovo.ru/home")
        
    def add_summatives(self):
        # https://student.letovo.ru/?r=student&part_student=summative
        req = self._student_letovo_home()
        req = self._request_student_html("https://student.letovo.ru/student/academic/summatives")
        req = self._request_student_html("https://student.letovo.ru/?r=student&part_student=summative")
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        if soup.find(id="table_fix") is None:
            return
        table_fix = soup.find(id="table_fix").find("tbody")
        for tr in table_fix.find_all("tr"):
            found = tr.find_all("td")
            date = datetime.datetime.strptime(found[0].text, "%Y-%m-%d")
            subject = found[1].text
            group = found[2].text
            theme = found[3].text
            criterias = re.compile(r"([A-D])").findall(found[4].text)
            if date <= self.schedule[6].date:
                for i in range(0, len(self.schedule[date.weekday()].lessons)):
                    if self.schedule[date.weekday()].lessons[i].name == subject:
                        break
                criterias_str = ""
                for j in criterias:
                    criterias_str += f"{j} "
                criterias_str = criterias_str[:-1]
                self.schedule[date.weekday()].add(Lesson({
                    "type": "event",
                    "name": f"""{theme}, критерии """ + criterias_str + " - самматив",
                    "room": self.schedule[date.weekday()].lessons[i].room,
                    "group_name": group,
                    "time_start": self.schedule[date.weekday()].lessons[i].time_start.strftime("%H:%M"),
                    "time_end": self.schedule[date.weekday()].lessons[i + (1 if self.schedule[date.weekday()].lessons[i+1].name == subject else 0)].time_end.strftime("%H:%M")
                }))
                
    def get_teachers(self):
        try:
            self._student_letovo_home()
            req = self._request_student_html("https://student.letovo.ru/student/1/studyplan")
            soup = bs4.BeautifulSoup(req.text, "html.parser")
            table_fix = soup.find(id="table_fix").find("tbody")
            res = []
            res_dict = {}
            for tr in table_fix.find_all("tr"):
                found = tr.find_all("td")
                dic = {
                    "group": re.compile(r"\b([А-Яа-яA-Za-z0-9.() -]+)\b").findall(found[0].text)[0],
                    "subject": re.compile(r"\b([А-Яа-яA-Za-z0-9.() ]+)\s").findall(found[1].text)[0],
                    "teacher": re.compile(r"\b([А-Яа-яA-Za-z0-9.() -]+)\b").findall(found[2].text)[0],
                    "hours_per_year": re.compile(r"(\d+)").findall(found[3].text)[0],
                    "hours_per_week": re.compile(r"(\d+)").findall(found[4].text)[0],
                    "level": re.compile(r"\b([А-Яа-яA-Za-z0-9.() -]+)\b").findall(found[5].text)[0],
                    "type": re.compile(r"\b([А-Яа-яA-Za-z0-9.() -]+)\b").findall(found[6].text)[0]
                }
                res.append(dic)
                res_dict[dic["subject"]] = dic
            self.teachers_list = res
            self.teachers_dict = res_dict
            self.got_teachers = True
            return res
        except:
            self.got_teachers = False
        
    def __init__(self, login = None, password = None):
        self.student_phpsessid = None
        self.init(login, password)
        
    def init_from_dict(self, student: dict = None):
        self.firstname = student["firstname_ru"] if student["firstname_ru"] is not None else student["firstname_en"]
        self.lastname = student["lastname_ru"] if student["lastname_ru"] is not None else student["lastname_en"]
        self.middlename = student["middlename_ru"] if student["middlename_ru"] is not None else student["middlename_en"]
        self.gender = student["gender"]
        self.class_n = student["enrollee_class_id"]
        self.id = student["id"]
        self.email: str = student["email"]
        
    def me(self):
        req = self._request_post("https://elk.letovo.ru/api/me")
        return req.json()
    
    def init(self, login = None, password = None):
        self.session = requests.session()
        if not "@" in login: 
            login = f"{login}@student.letovo.ru"
        if not self.login(login, password):
            throw Exception("Login failed")
        self.login_student_letovo()
        self.schedule = self.get_schedule()
        self.init_from_dict(self.me()["user"])
    
    def login(self, login: str = None, password: str = None) -> bool:
        if login is None or password is None:
            print("-------------------------------")
            login = input("Please enter your login: ")
            choice = input(f"Is your login {login}?(y/n)")
            while choice.lower() != "y":
                login = input("Please enter your login: ")
                choice = input(f"Is your login {login}?(y/n)")
            password = input("Please enter your password: ")
            choice = input(f"Is your password {password}?(y/n)")
            while choice.lower() != "y":
                password = input("Please enter your password: ")
                choice = input(f"Is your password {password}?(y/n)")
            print("-------------------------------")
        self.email = login
        self.password = password
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
        req = self._request_get("https://elk.letovo.ru")
        data = json.dumps({"email":login, "password":password, "params":[]})
        req = self._request_post("https://elk.letovo.ru/api/login", data=data, headers={"Content-Type": "application/json;charset=UTF-8"})
        if req.status_code == 401:
            logging.error("Login failed")
            return False
        else:
            logging.info("Login successful")
            return True
