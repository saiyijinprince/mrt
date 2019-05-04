from datetime import datetime

class Station:
    def __init__(self, code:str, name:str, date:str):
        self.code = code 
        self.name = name
        self.date = date
        self.line = self.code[0:2]

    def isOpen(self) -> bool:
        try:
            dateTimeToday = datetime.today()
            dateToday = dateTimeToday.date()
            stationDate = datetime.strptime(self.date, "%d %B %Y").date()
            return stationDate < dateToday
        except ValueError:
            return False

