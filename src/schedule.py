import requests
import logging
import datetime
import eatings as eating
import json
import re
import regex
import bs4

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
        self.table: Week = None
        
    def get_schedule(self) -> "Week":
        today = datetime.datetime.today()
        weekday = today.weekday()
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
        self.table = res
        return res

class StudentLetovo(Schedule):
    def login_student_letovo(self, login: str = None, password: str = None):
        self.student_login = login
        self.student_password = password
        if login is None:
            self.student_login = self.email.split('@')[0]
        if password is None:
            self.student_password = self.password
        verify = False # Set to False when using a proxy

        r_csrf = self.session.get("https://student.letovo.ru/login", verify=verify)
        cookies = r_csrf.headers.get("Set-Cookie")
        phpsessid = regex.search("(?<=PHPSESSID=)[a-zA-Z0-9]+", cookies).group(0)
        csrf = regex.search("(?<=_token( )*:( )*')[a-zA-Z0-9]+", r_csrf.text).group(0)
        # print("CSRF: " + csrf)
        # username = input("username: ")
        # password = input("password: ")
        username = self.student_login
        password = self.student_password
        r_login = self.session.post("https://student.letovo.ru/login", data=f"_token={csrf}&login={username}&password={password}", headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Csrf-Token": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
        }, cookies={
            "PHPSESSID": phpsessid
        }, verify=verify)
        self.student_phpsessid = phpsessid
        self.student_csrf = csrf

        # print("PHPSESSID: " + phpsessid)

    def _student_letovo_home(self):
        return self.session.get("https://student.letovo.ru/home", headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
        }, cookies = {
            "PHPSESSID": self.student_phpsessid
        })
        
    def add_summatives(self):
        # https://student.letovo.ru/?r=student&part_student=summative
        self._student_letovo_home()
        req = self.session.get("https://student.letovo.ru/student/academic/summatives", headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
        }, cookies = {
            "PHPSESSID": self.student_phpsessid
        })
        req = self.session.get("https://student.letovo.ru/?r=student&part_student=summative", headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
        }, cookies={
            "PHPSESSID": self.student_phpsessid
        })
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        table_fix = soup.find(id="table_fix").find("tbody")
        for tr in table_fix.find_all("tr"):
            found = tr.find_all("td")
            date = datetime.datetime.strptime(found[0].text, "%Y-%m-%d")
            subject = found[1].text
            group = found[2].text
            theme = found[3].text
            criterias = re.compile(r"([A-D])").findall(found[4].text)
            if date <= self.table[6].date:
                for i in range(0, len(self.table[date.weekday()].lessons)):
                    if self.table[date.weekday()].lessons[i].name == subject:
                        break
                criterias_str = ""
                for j in criterias:
                    criterias_str += f"{j} "
                criterias_str = criterias_str[:-1]
                self.table[date.weekday()].add(Lesson({
                    "type": "event",
                    "name": f"""{theme}, критерии """ + criterias_str + f" - самматив",
                    "room": self.table[date.weekday()].lessons[i].room,
                    "group_name": group,
                    "time_start": self.table[date.weekday()].lessons[i].time_start.strftime("%H:%M"),
                    "time_end": self.table[date.weekday()].lessons[i + (1 if self.table[date.weekday()].lessons[i+1].name == subject else 0)].time_end.strftime("%H:%M")
                }))
                
    def get_teachers(self):
        self._student_letovo_home()
        req = self.session.get("https://student.letovo.ru/student/1/studyplan", headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
        }, cookies = {
            "PHPSESSID": self.student_phpsessid
        })
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        table_fix = soup.find(id="table_fix").find("tbody")
        res = []
        for tr in table_fix.find_all("tr"):
            found = tr.find_all("td")
            res.append({
                "group": found[0].text,
                "subject": found[1].text,
                "teacher": found[2].text,
                "hours_per_year": found[3].text,
                "hours_per_week": found[4].text,
                "level": found[5].text,
                "theme": found[6].text,
                "type": found[7].text
            })
        self.teachers_dict = res
        return res
        
    def __init__(self, login = None, password = None):
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
        req = self.session.post("https://elk.letovo.ru/api/me", headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"})
        return req.json()
    
    def add_eatings(self):
        monday = eating.get_eatings_monday(self.class_n)
        tuesday_friday = eating.get_eatings_tuesday_friday(self.class_n)
        saturday = eating.get_eatings_saturday(self.class_n)
        sunday = eating.get_eatings_sunday(self.class_n)
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
        
    def init(self, login = None, password = None):
        self.session = requests.session()
        self.login(login, password)
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
        req = self.session.get("https://elk.letovo.ru")
        # req = self.session.get("https://elk.letovo.ru/js/jquery.min.js")
        # req = self.session.get("https://elk.letovo.ru/js/jquery-ui.js")
        # req = self.session.get("https://elk.letovo.ru/js/datepicker-ru.js")
        # req = self.session.get("https://elk.letovo.ru/js/app.js")
        # req = self.session.get("https://elk.letovo.ru/js/svg.js")
        # req = self.session.get("https://elk.letovo.ru/js/8602.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/rocketchat-livechat.min.js")
        # req = self.session.get("https://elk.letovo.ru/js/3335.js")
        # req = self.session.get("https://chat.letovo.ru/livechat")
        # req = self.session.get("https://elk.letovo.ru/apple-touch-icon.png")
        # req = self.session.get("https://elk.letovo.ru/favicon.svg")
        # req = self.session.get("https://chat.letovo.ru/livechat/34248.85b13.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/polyfills.a34ad.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/77487.6fb16.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/bundle.c3f51.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/88157.chunk.7aaa4.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/2728.chunk.18521.css")
        # req = self.session.get("https://chat.letovo.ru/livechat/2728.chunk.3d2fa.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/39537.chunk.a4bdf.js")
        # req = self.session.get("https://chat.letovo.ru/api/v1/livechat/config")
        # req = self.session.get("https://chat.letovo.ru/livechat/50482.chunk.714f6.js")
        # req = self.session.get("https://chat.letovo.ru/livechat/86443.chunk.15f26.js")
        # req = self.session.get("https://chat.letovo.ru/sounds/chime.mp3")
        data = json.dumps({"email":login, "password":password, "params":[]})
        req = self.session.post("https://elk.letovo.ru/api/login", data=data, headers={
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
        }, verify=False)
        if req.status_code == 401:
            logging.error("Login failed")
            return False
        else:
            logging.info("Login successful")
            return True
        
    