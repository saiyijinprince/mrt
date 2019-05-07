from station import Station
from date_utils import DateUtils
from queue import Queue

class StationMap:
    """Utility class that will facilitates various operations for load and routing stations.
    
    Attributes
    ----------
    stations: dict
        A dictionary that's keyed off of the station code (e.x. CC19) and the mapped value is a station object
    stationsGraph: dict
        A graph representation of the entire system as an adjacency list
    stationInterchanges: dict
        A dict that represents stations that have interchanges.  The key is the name of the station, and the value is 
        a list of station codes which are all available at that station

    Methods
    -------
    findRoute(self, source:str, target:str, option:str = None, startTime:str = None)
        Finds a route from source station to target station.  Depending on the options it will return
        the shortest path or the shortest time route
    
    formateRoutesForPrinting(self, routes:[])
        Will return an array list of displayableRoute object.  Used by both command line util and webapp
        to print the route information easier.
    """

    dateUtils = DateUtils()
    def __init__(self, stationMapDataFilePath: str) -> None:
        """
        Parameters
        ----------
        stationMapDataFilePath: str
            input data file that contains all the stations information such as there codes, the construction date
            and interchange information.  Everything that's needed to build the stations graph.
        """
        f = open(stationMapDataFilePath, "r")
        if f.mode != 'r':
            print("Error reading input file")
        lines = f.readlines()

        self.stations = {}
        self.stationGraph = {}
        self.stationInterchanges = {}

        self.__parseInputStationsData(lines)

    def findRoute(self, source:str, target:str, option:str = None, startTime:str = None) -> []:
        """
        Finds a route from source station to target station.

        Parameters
        ----------
        source: str
            The starting station name.

        target: str
            The destination station name.

        option: str, optional
            Controls which type of routing to perform.
            "fastest"(default): Returns the route with the least stops.  Ignores timings.
            "shortest": Returns all routes, with the travel time (in minutes). 
        
        startTime: str, optional
            Search for a route for a specific time.  Defaults to the current time if none is specified

        Returns
        -------
        list
            A list of tuples representing where the first index represents all stops of the route and the 
            second index represents the travel time.  If the option "shortest" was selected the travel 
            time will be empty.
        """
        
        if (source not in self.stationInterchanges or target not in self.stationInterchanges):
            print("Invalid inputs")
            return []

        if not option:
            option = 'shortest'

        # You can have multiple sources and destinations because the station can be an 
        # interchange where you have multiple lines to chose from. 
        sources = self.stationInterchanges[source]
        dests = self.stationInterchanges[target]

        route = []
        if option == 'shortest':
            route = self.__findRouteShortestPath(sources, dests)
        elif option == 'fastest':
            if not startTime or len(startTime) == 0:
                startTime = StationMap.dateUtils.getTodaysDate()
            route = self.__scheduleRoute(sources, dests, startTime)
        else:
            print('Invalid option: {0}'.format(option))
            return []
        return route

    def formateRoutesForPrinting(self, routes:[]) -> []:
        if (len(routes) == 0):
            return
        
        #TODO: Encapsulate Displayable route in a class.
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
        routesDisplay = self.formateRoutesForPrinting(routesInfo)

        for rd in routesDisplay:
            print('Route #{0}'.format(rd['id']))
            print(rd['header'])
            print(rd['desc'])
            print(rd['summary'])
      
            for step in rd['routeSteps']:
                print(step)
            print('\n')


    def __scheduleRoute(self, sources:[], dests:[], startTime:str) -> []:
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

            #TODO: Future enhancement add timestamp for each stop.  Also mark which parts of the route are during peak hours.
            visited.add(curr)
            path.append(curr)
            
            if curr in destinations:
                timeTaken = StationMap.dateUtils.minuteDifference(startTime, elapsedTime)
                results.append((list(path), str(timeTaken)))
                continue
            
            interchanges = Queue()
            neighbors = self.stationGraph[curr]
            currStation = self.stations[curr]
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

    def __findRouteShortestPath(self, sources:[], dests:[]) -> []:

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

    def __addEdge(self, station1:str, station2:str):
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

    def __addEdges(self, station:str, stations:[]):
        for s in stations:
            self.__addEdge(station, s)
      
    def __parseInputStationsData(self, lines:[]) -> None:
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

            # Check is the station has been constructed already
            if not self.stations[station].isOpen():
                continue

            # Builds the station graph
            nameLower = name.lower()
            if nameLower in self.stationInterchanges:
                self.stationInterchanges[nameLower].append(station)
                self.__addEdges(station, self.stationInterchanges[nameLower])
            else:
                self.stationInterchanges[nameLower] = [station]
            
            if (prevLine != currLine):
                prevStation = ''

            if prevStation:
                self.__addEdge(prevStation, station)

            prevStation = station
            prevLine = currLine



