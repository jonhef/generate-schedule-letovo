import requests
import logging
import datetime

class Week:
    def __init__(self, week: "list[Day]", date: datetime.datetime) -> None:
        self._week = week
        self._date = date
        
    def __getitem__(self, key: int) -> "Day":
        return self._week[key]

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
    
    def time(self) -> int:
        return self.time_start.hour * 60 * 60 + self.time_start.minute * 60 + self.time_start.second
    
class HomeWork(Task):
    def __init__(self, homework: dict):
        super().__init__(homework)
        
    def __str__(self) -> str:
        return f"{self.name} ({self.room})"
    
class Eating(Task):
    def __init__(self, eating: dict):
        super().__init__(eating)
        
    def __str__(self) -> str:
        return f"{self.name} ({self.room})"

class Lesson(Task):
    def __init__(self, lesson: dict):
        super().__init__(lesson)
        
    def __str__(self) -> str:
        return f"{self.name} ({self.room})"

class Schedule:
    def __init__(self):
        self.table = None
        
    def get_schedule(self) -> "list[list[Lesson]]":
        today = datetime.datetime.today()
        weekday = today.weekday()
        if weekday != 0:
            today = today - datetime.timedelta(days=weekday)
        res = []
        for i in range(0, 7):
            req = self.session.get(f"https://elk.letovo.ru/api/education_track/schedule?date={today.year}-{today.month}-{today.day}")
            if req.status_code != 200:
                logging.error("Failed to get schedule")
                res.append([])
                continue
            obj = req.json()
            for j in obj:
                if j["type"] == "lesson":
                    res.append(Lesson(j))
            today = today + datetime.timedelta(days=1)
        self.table = res
        return res
    
    

class StudentLetovo:
    def __init__(self):
        self.session = requests.session()
    
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
        req = self.session.post("https://elk.letovo.ru/api/login", data="{\"email\": " + login + ", \"password\": " + password + ", \"params\" = []}")
        if req.status_code == 401:
            logging.error("Login failed")
            return False
        else:
            logging.info("Login successful")
            return True
        
    