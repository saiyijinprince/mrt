#!/usr/bin/python

import sys, getopt
from station_map import StationMap
from datetime import datetime

def main(argv):
    inputFile = './StationMap.csv'
    option = 'shortest'
    source = ''
    target = ''
    time = ''
    helpMsg = 'usage: zendesk.py -s <start station> -d <target station> [-o <option=[shortest,fastest] -t <startTime=[current_time]> -i <path/to/stationmap=./StationMap.csv>]' 
    try:
        opts, args = getopt.getopt(argv, "i:s:d:h:o:t:")
    except getopt.GetoptError:
        print (helpMsg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputFile = arg
        elif opt == "-s":
            source = arg.lower()
        elif opt == "-d":
            target = arg.lower()
        elif opt == "-o":
            option = arg.lower()
        elif opt == '-t':
            time = arg
        elif opt == "-h":
            print (helpMsg)
            sys.exit()

    print ('Input file:{0}'.format(inputFile))

    if not source or not target:
        print('Missing required parameters: -s <source> or -d <destinatin>\n{0}'.format(helpMsg))
        sys.exit(2)

    stationMap = StationMap(inputFile)
    route = stationMap.findRoute(source, target, option, time)
    stationMap.printRoute(route)

if __name__ == "__main__":
    main(sys.argv[1:])
