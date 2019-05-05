from station_datetime_utils import StationDatetimeUtils

class Station:

    stationDatetimeUtils = StationDatetimeUtils()

    def __init__(self, code:str, name:str, date:str):
        self.code = code 
        self.name = name
        self.date = date
        self.line = self.code[0:2]

    def isOpen(self) -> bool:
        try:
            #Check whether the station has completed construction
            return Station.stationDatetimeUtils.isDatePriorToday(self.date)
        except ValueError:
            return False
    
    def isOpenAtSpecificTime(self, inputTime:str = None) -> bool:
        try:
            if Station.stationDatetimeUtils.compareDates(self.date, '%d %B %Y', inputTime, '%Y-%m-%dT%H:%M') > -1:
                return False
            #Is the input time between 10PM - 6AM, if so then station will be closed
            return Station.stationDatetimeUtils.isLineRunning(self.line, inputTime)

        except ValueError:
            return False

    def addStationInterchangeTime(self, inputTime:str) -> str:
        return Station.stationDatetimeUtils.addStationInterchangeTime(inputTime)
        
    def getStationTravelTime(self, inputTime:str) -> str:
        return Station.stationDatetimeUtils.getNextTrainTime(inputTime, self.line)

