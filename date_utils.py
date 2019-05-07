from datetime import datetime, time, timedelta

class DateUtils:
    def isTimeBetween(self, beginTime:time, endTime:time, inputTime:time) -> bool:
        if beginTime < endTime:
            return inputTime >= beginTime and inputTime <= endTime
        else:
            return inputTime >= beginTime or inputTime <= endTime

    def addMinutes(self, currentDate:str, dateFormat:str,  mins:int) -> str:
        """
        Add the the number of minutes represented by min to the currentDate input and 
        returns that new date timestamp
        """
        inputDateTime = datetime.strptime(currentDate, dateFormat)
        nextTime = inputDateTime + timedelta(minutes=mins)
        return nextTime.strftime(dateFormat)

    def minuteDifference(self, begin:str, end:str) -> str:
        dateFormat = '%Y-%m-%dT%H:%M'

        beginDateTime = datetime.strptime(begin, dateFormat)
        endDateTime = datetime.strptime(end, dateFormat)

        diff = endDateTime - beginDateTime
        return diff.total_seconds() / 60.0

    def getTodaysDate(self, dateFormat:str = None) -> str:
        if not dateFormat:
            dateFormat = '%Y-%m-%dT%H:%M'
        return datetime.today().strftime(dateFormat)

    def compareDates(self, date1:str, date1Format:str, date2:str, date2Format:str) -> int:
        """
        Performs comparisons between two dates.

        Parameters
        ----------
        date1: str
            The first date to be compared with.
        
        date1Format: str
            The date format that date1 is in.

        date2: str
            The second date to compare against.

        date2Format:
            The date format that date2 is in.

        Returns
        -------
            int: -1,0,1,2
                -1: represents date1 comes before date2
                 0: represents date1 and date2 are the same
                 1: represents date1 does not come before date2
                -2: error condition, inputs were invalid and could not be parsed 

        """
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