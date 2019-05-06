from station import Station
from date_utils import DateUtils
from queue import Queue

class StationMap:
    dateUtils = DateUtils()
    def __init__(self, stationMapDataFilePath: str):
        f = open(stationMapDataFilePath, "r")
        if f.mode != 'r':
            print("Error reading input file")
        lines = f.readlines()

        self.stations = {}
        self.stationGraph = {}
        self.stationInterchanges = {}

        prevStation = ''
        prevLine = ''
        count = -1
        
        for line in lines:
            count += 1
            if count == 0:
                continue

            station, name, date = line.split(',')
            currLine = station[:2]        
            if station in self.stations:
                continue

            self.stations[station] = Station(code=station, name=name, date=date.rstrip())
            if not self.stations[station].isOpen():
                continue

            if name in self.stationInterchanges:
                self.stationInterchanges[name].append(station)
                self.addEdges(station, self.stationInterchanges[name])
            else:
                self.stationInterchanges[name] = [station]
            
            if (prevLine != currLine):
                prevStation = ''

            if prevStation:
                self.addEdge(prevStation, station)

            prevStation = station
            prevLine = currLine
    
    def addEdge(self, station1:str, station2:str):
        if (station1 == station2):
            return
        if station1 not in self.stationGraph:
            self.stationGraph[station1] = set()
        if station2 not in self.stationGraph:
            self.stationGraph[station2] = set()

        if (station2 not in self.stationGraph[station1]):
            self.stationGraph[station1].add(station2)
        if (station1 not in self.stationGraph[station2]):
            self.stationGraph[station2].add(station1)

    def addEdges(self, station:str, stations:[]):
        for s in stations:
            self.addEdge(station, s)

    def findRoute(self, source:str, target:str, option:str = None, startTime:str = None) -> []:
        if (not source or not target):
            print("Invalid input")
            return []

        if (source not in self.stationInterchanges or target not in self.stationInterchanges):
            print("Invalid inputs")
            return []

        if not option:
            option = 'shortest'

        route = []
        if option == 'shortest':
            route = self.findRouteShortestPath(source, target)
        elif option == 'fastest':
            if not startTime or len(startTime) == 0:
                startTime = StationMap.dateUtils.getTodaysDate()
            route = self.scheduleRoute(source, target, startTime)
        else:
            print('Invalid option')
            return []
        return route

    def scheduleRoute(self, source:str, dest:str, startTime:str) -> []:
        if (source == dest):
            return []

        sources = self.stationInterchanges[source]
        dests = self.stationInterchanges[dest]
        destinations = set(dests)
        results = []
        visited = set()

        q = Queue()
        for s in sources:
            currStation = self.stations[s]
            if (currStation.isOpenAtSpecificTime(startTime)):
                q.put((s, [], startTime))

        while not q.empty():
            (curr, path, elapsedTime) = q.get()
            if curr in visited:
                continue

            visited.add(curr)
            path.append(curr)
            currStation = self.stations[curr]
            
            if curr in destinations:
                timeTaken = StationMap.dateUtils.minuteDifference(startTime, elapsedTime)
                results.append((list(path), str(timeTaken)))
                continue
            
            interchanges = Queue()
            neighbors = self.stationGraph[curr]
            for n in neighbors:
                nextStation = self.stations[n]

                if n in visited:
                    continue

                #If there are interchange stations, always add the stations that's on same line first
                if currStation.line == nextStation.line:
                    arrivalTime = nextStation.getStationTravelTime(elapsedTime)
                    if nextStation.isOpenAtSpecificTime(arrivalTime):
                        q.put((n, list(path), arrivalTime))
                else:
                    #Add time to interchange time to the arrival time
                    arrivalTime = currStation.addStationInterchangeTime(elapsedTime)
                    arrivalTime = nextStation.getStationTravelTime(elapsedTime)
                    if nextStation.isOpenAtSpecificTime(arrivalTime):
                        interchanges.put((n, list(path), arrivalTime))

            while not interchanges.empty():
                q.put(interchanges.get())                

        return results

    def findRouteShortestPath(self, source:str, dest:str) -> []:
        if source == dest:
            return []

        #throw exception if input isn't found
        sources = self.stationInterchanges[source]
        dests = self.stationInterchanges[dest]
        destinations = set(dests)
        minPath = []
        visited = set()
        
        q = Queue()
        for s in sources:
            q.put((s, list([])))

        while not q.empty():
            (curr, path) = q.get()
            if curr in visited:
                continue

            visited.add(curr)
            path.append(curr)

            if curr in destinations:
                if len(minPath) == 0:
                    minPath.append((list(path),''))    
                elif len(path) < len(minPath[0][0]):
                    minPath[0] = (list(path),'')

            neighbors = self.stationGraph[curr]
            interchanges = Queue()
            for n in neighbors:
                if n in visited:
                    continue
                #If there are interchange stations, always add the stations that's on same line first
                if self.stations[curr].line == self.stations[n].line:
                    q.put((n, list(path)))
                else:
                    interchanges.put((n, list(path)))

            while not interchanges.empty():
                q.put(interchanges.get())

        return minPath

    def formateRoutesForPrintig(self, routes:[]) -> []:
        if (len(routes) == 0):
            return
        
        displayableRoutes = []
        displayableRoute = {}
        for i, ri in enumerate(routes):
            if len(ri) != 2:
                continue
            
            displayableRoute['id'] = i
            route = ri[0]
            travelTime = ri[1]

            prevStation = self.stations[route[0]]
            lastStation = self.stations[route[-1]]

            displayableRoute['header'] = 'Travel from {0} to {1}'.format(prevStation.name, lastStation.name)
            if len(travelTime) == 0:
                displayableRoute['desc'] = 'Stations travelled: {0}'.format(len(route))
            else:
                displayableRoute['desc'] = 'Time: {0} minutes'.format(travelTime)
            
            displayableRoute['summary'] = 'Route: {}'.format(route)
            routeSteps = []
            for j in range(1, len(route)):
                station = self.stations[route[j]]
                if prevStation.line != station.line:
                    routeSteps.append('Change from {0} line to {1} line'.format(prevStation.line, station.line))
                else:
                    routeSteps.append('Take {0} line from {1} to {2}'.format(station.line, prevStation.name, station.name))
                prevStation = station
            
            displayableRoute['routeSteps'] = list(routeSteps)
            displayableRoutes.append(dict(displayableRoute))
        return displayableRoutes
    
    def printRoute(self, routesInfo:[]):
        routesDisplay = self.formateRoutesForPrintig(routesInfo)

        for rd in routesDisplay:
            print('Route #{0}'.format(rd['id']))
            print(rd['header'])
            print(rd['desc'])
            print(rd['summary'])
      
            for step in rd['routeSteps']:
                print(step)
            print('\n')
                  





