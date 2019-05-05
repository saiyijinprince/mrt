from datetime import datetime, time, timedelta

class DateUtils:
    def isTimeBetween(self, beginTime:time, endTime:time, inputTime:time) -> bool:
        if beginTime < endTime:
            return inputTime >= beginTime and inputTime <= endTime
        else:
            return inputTime >= beginTime or inputTime <= endTime

    def addMinutes(self, currentDate:str, dateFormat:str,  mins:int) -> str:
        inputDateTime = datetime.strptime(currentDate, dateFormat)
        nextTime = inputDateTime + timedelta(minutes=mins)
        return nextTime.strftime(dateFormat)

    def minuteDifference(self, begin:str, end:str) -> str:
        dateFormat = '%Y-%m-%dT%H:%M'

        beginDateTime = datetime.strptime(begin, dateFormat)
        endDateTime = datetime.strptime(end, dateFormat)

        diff = endDateTime - beginDateTime
        return diff.total_seconds() / 60.0