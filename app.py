from flask import Flask, render_template, request
from station_map import StationMap

app = Flask(__name__)

stationMap = StationMap('./StationMap.csv')

@app.route('/')
def home() -> 'html':
	return render_template('index.html', page_title='Zendesk\'s MRT System', stationMap=stationMap)

@app.route('/findRoute', methods=['POST'])
def findRoute() -> 'html':
	source = request.form['source']
	dest = request.form['dest']
	option = request.form['option']
	time = request.form['time']

	routes = stationMap.findRoute(source, dest, option, time)
	routesDisplay = stationMap.formateRoutesForPrinting(routes)

	if len(routes) == 0:
		return render_template('no_routes.html', results_title='No Routes Found', routes=routes)
	else:
		return render_template('results.html', results_title='Available Routes', routes=routesDisplay)

app.run()