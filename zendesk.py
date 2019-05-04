#!/usr/bin/python

import sys, getopt
from station_map import StationMap

def main(argv):
    inputFile = ''
    source = ''
    target = ''
    try:
        opts, args = getopt.getopt(argv, "i:s:d:h:")
    except getopt.GetoptError:
        print ('usage: zendesk.py -d <path/to/stationmap.csv')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputFile = arg
        elif opt == "-s":
            source = arg
        elif opt == "-d":
            target = arg
        elif opt == "-h":
            print ('zendesk.py -s <path/to/stationmap.csv>')
            sys.exit()
    print ('Input file:', inputFile)

    stationMap = StationMap(inputFile)
    route = stationMap.findRouteShortestPath(source, target)
    
    stationMap.printRoute(route)
    #print(stationMap.stationExchanges)

if __name__ == "__main__":
    main(sys.argv[1:])
