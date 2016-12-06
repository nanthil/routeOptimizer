import csv
import gc
import json
#TODO
# in formatStopData()
#	implement measure distance by some location
#	i.e. gps, address, lat/long etc
#location finding and getting should be a module unto itself

#This file reads rtd data
#To use:
#	Call getSomethingBySomething(arguments)
#	getSomethingBySomething(args) returns the results of readCsv(func, filename, args)
#		func is the data formatting function found in the implementation below
#		filname is the csv file you wish to read
#		args are the arguments you wish to pass, which may be any data format

#To extend:
#	create a getFunction(args) that takes 1 argument
#	call readCSV(formatData, 'filename.txt', args) where args are the filter for your data formatter
#	def formatData(row, args, results): return results

def readCsv(function, fileName, args):
	results = {}
	reader = csv.DictReader(open(fileName))
	#TODO remove implicit iteration
	for row in reader:
		results = function(row, args, results)	
	return results

#getStopsByLocation(location) takes a location
#returns:
#{
#	stop_id: {
#		lat: string,
#		long: string,
#		etc...
#	}
#}
def getStopsByLocation(location):
	return readCsv(formatStopData, '../data/stops.txt', location)
#getAllStopTimeDataForListOfStops(list) takes a list of stops
#returns:
#{ 
#	stop_id: { 
#		arrival_times: [data, data, data...],
#		departure_times: [data, data, data...],
#		drop_off_type: '',
#		etc...
#	}
#}
def getTripsByStopId(list_stopId):
	return readCsv(formatStopTimes, '../data/stop_times.txt', list_stopId)

#getRoutesByTripId(id) takes a trip id
#returns:
#{ routes: [route_id, route_id...]
def getRoutesByTripId(list_tripId):
	return readCsv(formatTrips, '../data/trips.txt', trip_id)

#getRoutes(list_route) takes a route id	
#returns:
# { route_id : { key: data, key:data, key: data, etc...},
#	route_id : {...},
#	etc...
# }
def getRoutes(list_routeId):
	return readCsv(formatRoutes, '../data/routes.txt', list_routeId)




#begin implementation
def formatStopData(row, location, results):
	if row['stop_id'] not in results:
		results[row['stop_id']] = {}
			
	#create empty keys in our dict
	for k in row:
		if k != 'stop_id':
			results[row['stop_id']][k] = ''

	#fill keys in our dict
	for k in results[row['stop_id']]:
		if k in results[row['stop_id']]:
			results[row['stop_id']][k] = row[k]

	return results

#stop ids for testing
#['12241', '19189', '25458', '25459', '22526', '22527', '26588', '22602', '13043', '23393', '13042', '13040', '25124', '25126']
def formatStopTimes(row, list_stopids, results):
	if row['stop_id'] in list_stopids:
		if row['stop_id'] not in results:
			#rows intended to have more than 1 unique value
			#end in 's' for plural
			results[row['stop_id']] = {
			'arrival_times': [],
			'departure_times': [],
			'trip_ids': [],
			'drop_off_type': '',
			'shape_dist_traveled': '',
			'pickup_type': '',
			'stop_sequences': [],
			'stop_headsign': '',
			}
		for k in results[row['stop_id']]:
			if k[-1:] == 's' and row[k[:-1]] not in results[row['stop_id']][k]:
				results[row['stop_id']][k].append(row[k[:-1]])
			elif k[-1:] != 's':
				results[row['stop_id']][k] = row[k]
	return results

def formatTrips(row, trip_id, results):
	if row['trip_id'] in trip_id:
		if 'route_ids' not in results:
			results['route_ids'] = []
		if	row['route_id'] not in results['route_ids']: 
			results['route_ids'].append(row['route_id'])
	return results
#print(getRoutesByTripId(['110497350', '110497351', '110497352', '110498191', '110498192', '110498193', '110498194', '110498200', '110498201', '110498202', '110498203']))

def formatRoutes(row, route_ids, results):
	for rid in route_ids:
		if row['route_id'] in route_ids:
			if rid not in results:
				results[rid] = {} 
	
			for k in row:
				if k != rid:
					results[rid][k] = row.get(k)
		
	return results 
#print(getRoutes(['15', '15L', 'JUMP']))
