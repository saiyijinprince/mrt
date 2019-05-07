from station_datetime_utils import StationDatetimeUtils
from date_utils import DateUtils

class Station:
    """
    A class that encapsulates all of the station metadata.  It also provides methods to determine
    the timing based for travel and interchange times.

    Attributes
    ----------
    code: str
        The station code (e.x. NE21)
    name: str
        The full station name
    date: str
        The date the station was constructed
    line: str
        The station line (e.x. NE)

    Methods
    -------
    isOpen() -> bool:
        Returns whether the station has been constructed.

    isOpenAtSpecificTime(self, inputTime:str = None) -> bool:
        Returns wether the station has been constructed already with respect to the input time

    addStationInterchangeTime(self, inputTime:str) -> str:
        Given the inputTime, it will return a new timestamp adding the additional interchange time

    getStationTravelTime(self, inputTime:str) -> str:
        Given the inputTime, it will return a new timestamp adding the additional interchange time
    """

    stationDatetimeUtils = StationDatetimeUtils()
    dateUtils = DateUtils()

    def __init__(self, code:str, name:str, date:str):
        self.code = code 
        self.name = name
        self.date = date
        self.line = self.code[0:2]

    def isOpen(self) -> bool:
        """
        Returns whether the station has been constructed already, comparing against today's date.

        Returns
        -------
        bool
            True/False.
        """
        try:
            #Check whether the station has completed construction
            return Station.stationDatetimeUtils.isDatePriorToday(self.date)
        except ValueError:
            return False
    
    def isOpenAtSpecificTime(self, inputTime:str = None) -> bool:
        try:
            if Station.dateUtils.compareDates(self.date, '%d %B %Y', inputTime, '%Y-%m-%dT%H:%M') > -1:
                return False
            #Is the input time between 10PM - 6AM, if so then station will be closed
            return Station.stationDatetimeUtils.isLineRunning(self.line, inputTime)

        except ValueError:
            return False

    def addStationInterchangeTime(self, inputTime:str) -> str:
        return Station.stationDatetimeUtils.addStationInterchangeTime(inputTime)
        
    def getStationTravelTime(self, inputTime:str) -> str:
        return Station.stationDatetimeUtils.getNextTrainTime(inputTime, self.line)

