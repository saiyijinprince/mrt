# Directions For Running Program


## Option #1: CLI Program
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
        3. The application will run on your local machine.  Open chrome or firefox and go to url flask provided.  (Most likely: http://127.0.0.1:5000/)


**Approach For Finding Route**
1. Shortest Path  
The shortest path algorithm does not take any timings into consideration.  It simply does a BFS search and will return the path with the least amount of stop.

2. Fastest Path  
The fast path algorithm will use the input time as the time you get on the  train of the source station.  Then will add timings for each stops and interchanges depending on the hours and the lines.  I chose to keep the timing information outside of the graph (i.e. Use the timeings as edges in the graph) and do the calculations while I am performing the BFS because almost all the timings are equal so to save some memory, I calculate the timings on the fly depending on only line information and peak hours info defined by the problem. 

# Other Notes
I purposely left all files in the source directory to ensure everything runs properly out of the box and there was no need to install my local modules to site packages.  Usually I would define each module in a modules/<module_name>/ folder in which I can run a setup.py script and then install it into site packages to keep the source directory clean.  

This also made it easier to run the webapp without having to worry about running pip install.