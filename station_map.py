from station import Station
from queue import Queue

class StationMap:
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

        #print (self.stationInterchanges)
    
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
                if len(minPath) == 0 or len(path) < len(minPath):
                    minPath = list(path)

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
    
    def printRoute(self, route:[]):
        if (len(route) == 0):
            return
        
        prevStation = self.stations[route[0]]
        for i in range(1, len(route)):
            station = self.stations[route[i]]
            if prevStation.line != station.line:
                print ('Change from {0} line to {1} line'.format(prevStation.line, station.line))
            else:
                print ('Take {0} line from {1} to {2}'.format(station.line, prevStation.name, station.name))
            prevStation = station


"""
    def dfsShortestPath(self, s:str, d:[]) -> []:
        visited = set()
        currPath = []
        destinations = set(d)
        minPath = []
        

        def helper(currPath:[], minPath:[], curr:str, visited:set) -> bool:         
            if curr in visited:
                return False

            visited.add(curr)
            currPath.append(curr) 

            if curr in destinations:
                return True

            neighbors = self.stationGraph[curr]
            for n in neighbors:
                if helper(currPath, minPath, n, visited):
                    if len(minPath) == 0 or len(currPath) < len(minPath):
                        minPath = list(currPath)

            visited.remove(curr)
            del currPath[-1]
            return False

        helper(currPath, minPath, s, visited)
        return minPath
"""





