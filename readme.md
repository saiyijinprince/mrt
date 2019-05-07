# Directions For Running Program

## Note Project Directory Structure
Inside the zendesk folder, you'll find Python3/Python2 versions.  There are no differences other than the python 3 version includes function parameter types to help with hints while developing.  Since this will run on a fresh install on ubuntu 16.04, which comes with python 2 out of the box.  **Python3 is recommended for testing**  But if you aren't able to upgrade to python3 please use the Python2 folder.

## Option #1: CLI Program
**Python 3 is recommended**  

    Steps:
        1. cd to project directory
        2. run python zendesk.py  
            -s <start station> 
            -d <target station> 
            [-o <option=[shortest,fastest] 
             -t <startTime=[current_datetime]>
             -i <path/to/stationmap.csv=[./StationMap.csv]>]'  

    Required Params:
        -s <start station> 
        -d <target station>  
        
    Optional Params:
        -i <path/to/stationmap.csv>
        Default: ./StationMap.csv 

        -o <option>
        Default: Fastest

        -t <startTime>
        Default: Current time


    See sample scripts in current directory for example usage:
        cli_sample_with_times.sh
        cli_sample_without_times.sh


## Option #2: Web App
    
    Steps:
        0. Requires flask so to run the web app, run: "pip install flask"
        1. cd to project directory
        2. python app.py
        3. It will start running a local server.  Open chrome or firefox and go to url flask provided.  (Most likely: http://127.0.0.1:5000/)


**Approach For Finding Route**
1. Shortest Path  
The shortest path algorithm does not take any timings into consideration.  It simply does a BFS search and will return the path with the least amount of stops.

2. Fastest Path  
The fast path algorithm will use the input time as the time you get on the train of the first station.  Then timings are added for each stops and interchanges depending on the hours and the lines.  I chose to keep the timing information outside of the graph (instead the adding the timings as edges of the graph) and do the calculations while I am performing the BFS. This because almost all the timings are equal so to save some memory, I calculate the timings on the fly depending on the line information and peak hours defined by the problem. 

# Other Notes
1. I purposely left all files in the source directory to ensure everything runs properly out of the box and there is is no need to install my local modules to site packages.  Usually I would define each module in a modules/<module_name>/ folder in which I can run a setup.py script and then install it into site packages to keep the source directory clean.  This also made it easier to run the webapp.

2. Just wanted to point out a slightly interesting finding while testing.  In the examples.md file, the results with timings returned the results for:  
 Travel from Boon Lay to Little India during peak hours  
 Time: 150 minutes  
 Route: 
('EW27', 'EW26', 'EW25', 'EW24', 'EW23', 'EW22', 'EW21', 'CC22', 'CC21', 'CC20', 'CC19', 'DT9', 'DT10', 'DT11', 'DT12', 'NE7').  
**The destination for Little India is also DT12 given by the csv file so it looks like the output route double counted the destination station since it was an interchange station**