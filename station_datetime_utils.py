from datetime import datetime, time, timedelta
from date_utils import DateUtils

class StationDatetimeUtils:
    dateUtils = DateUtils()
    def __init__(self):
        self.inputDateFormat = '%Y-%m-%dT%H:%M'

    # Peak hours (6am-9am and 6pm-9pm on Mon-Fri)
    def isPeakHours(self, inputDate:str, inputDateFormat:str = None) -> bool:
        if not inputDateFormat:
            inputDateFormat = self.inputDateFormat

        inputDateTime = datetime.strptime(inputDate, inputDateFormat)

        # 0 - Monday, 6 - Sunday
        day = inputDateTime.weekday()

        #Weekends
        if (day > 5):
            return False

        inputTime = inputDateTime.time()
        #If weekday, then check if time is between 6am-9am or 6pm - 9pm
        if (StationDatetimeUtils.dateUtils.isTimeBetween(time(6,0), time(9,0), inputTime) 
            or StationDatetimeUtils.dateUtils.isTimeBetween(time(18,0), time(21,0), inputTime)):
            return True
        
        return False

    # Night hours (10pm-6am on Mon-Sun)
    def isNightHours(self, inputDate:str, inputDateFormat:str = None):
        if not inputDateFormat:
            inputDateFormat = self.inputDateFormat

        inputDateTime = datetime.strptime(inputDate, inputDateFormat)
        return StationDatetimeUtils.dateUtils.isTimeBetween(time(22,0), time(6,0), inputDateTime.time())

    def isDatePriorToday(self, inputDate:str, inputDateFormat:str = '%d %B %Y') -> bool:
        dateTimeToday = datetime.today()
        dateToday = dateTimeToday.date()
        stationDate = datetime.strptime(inputDate, inputDateFormat).date()
        return stationDate < dateToday
    
    def compareDates(self, date1:str, date1Format:str, date2:str, date2Format:str) -> int:
        try:            
            date1DateTime = datetime.strptime(date1, date1Format)
            date2DateTime = datetime.strptime(date2, date2Format)
            
            #Is the station built?
            if date1DateTime.date() < date2DateTime.date():
                return -1
            elif date1DateTime.date() > date2DateTime.date():
                return 1
            else:
                return 0

        except ValueError:
            return -2

    def isLineRunning(self, line:str, inputDate:str, inputDateFormat:str = None) -> bool:
        if not inputDateFormat:
            inputDateFormat = self.inputDateFormat
        if not inputDate:
            inputDateTime = datetime.today()
        else:
            inputDateTime = datetime.strptime(inputDate, inputDateFormat)

        inputTime = inputDateTime.time()
        if (StationDatetimeUtils.dateUtils.isTimeBetween(time(22,0), time(6,0), inputTime) 
            and (line in {'DT', 'CG', 'CE'})):
            return False

        return True

    def getNextTrainTime(self, inputTime:str, line:str) -> str:
        delta = 0
        if self.isPeakHours(inputTime):
            if line == 'NS' or line == 'NE':
                delta = 12
            else:
                delta = 10
        elif self.isNightHours(inputTime):
            if line == 'TE':
                delta = 8
            else:
                delta = 10
        else:
            if line == 'DT' or line == 'TE':
                delta = 8
            else:
                delta = 10

        return StationDatetimeUtils.dateUtils.addMinutes(inputTime, self.inputDateFormat, delta)

    def addStationInterchangeTime(self, currentTime:str) -> str:
        delta = 0
        if self.isPeakHours(currentTime):
            delta = 15
        else:
            delta = 10

        return StationDatetimeUtils.dateUtils.addMinutes(currentTime, self.inputDateFormat, delta)

