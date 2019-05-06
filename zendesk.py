#!/usr/bin/python

import sys, getopt
from station_map import StationMap
from datetime import datetime

def main(argv):
    inputFile = ''
    source = ''
    target = ''
    option = 'shortest'
    time = ''

    try:
        opts, args = getopt.getopt(argv, "i:s:d:h:o:t:")
    except getopt.GetoptError:
        print ('usage: zendesk.py -i <path/to/stationmap.csv> -s <start station> -d <target station> [-o <option=[shortest,fastest] -t <startTime>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputFile = arg
        elif opt == "-s":
            source = arg
        elif opt == "-d":
            target = arg
        elif opt == "-o":
            option = arg.lower()
        elif opt == '-t':
            time = arg
        elif opt == "-h":
            print ('zendesk.py -s <path/to/stationmap.csv>')
            sys.exit()
    print ('Input file:', inputFile)

    stationMap = StationMap(inputFile)
    route = stationMap.findRoute(source, target, option, time)
    stationMap.printRoute(route)

    #print(stationMap.stationExchanges)

if __name__ == "__main__":
    main(sys.argv[1:])
