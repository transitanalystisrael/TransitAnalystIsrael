#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# scan stops.txt to create train stops list with stop_id, stop name and location (lat, lon)
# output train_stops_gtfsdate.txt 
# output train_stops_gtfsdate.js 
#
import time
import csv
from geopy.distance import vincenty
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
	# input:
	parent_path = gtfsparentpath
	gtfsdir = gtfsdirbase+gtfsdate
	txtfilein = ''
	
	# output:
	txtfileout = 'train_stops'+'_'+gtfsdate+'.txt'
	jsfileout  = 'train_stops'+'_'+gtfsdate+'.js'
	
	gtfspathin = parent_path+gtfsdir+'\\'
	gtfspath = gtfspathin
	gtfspathout = pathout
	
	# >>> load routes file
	txtfilein = 'routes.txt'
	routes_list = []
	with open(gtfspathin+txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # [route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_color]
		print(header)
		for row in reader:
			#print row
			routes_list.append([row[0], row[1]]) # [route_id,agency_id]
	#print routes_list[:4]
	print('routes_list loaded. routes count ', len(routes_list))
	
	# >>> load trips file
	txtfilein = 'trips.txt'
	trips_list = []
	with open(gtfspathin+txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
		print(header)
		for row in reader:
			#print row
			trips_list.append([row[0], row[2]]) # [route_id,trip_id]
	#print trips_list[:4]
	print('trips_list loaded. trips count ', len(trips_list))
	
	# >>> load stop_times file
	txtfilein = 'stop_times.txt'
	stop_times_list = []
	with open(gtfspathin+txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # [trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled]
		print(header)
		for row in reader:
			#print row
			stop_times_list.append([row[0], row[3]]) # [trip_id,stop_id]
	#print stop_times_list[:4]
	print('stop_times_list loaded. stop_times count ', len(stop_times_list))
	
	# >>> load stops file
	txtfilein = 'stops.txt'
	stops_dict = {}
	with open(gtfspathin+txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'zone_id']
		print(header)
		for row in reader:
			#print row
			stops_dict[row[0]] = [row[2], row[3], row[4], row[5]] # 'stop_id' : ['stop_name', 'stop_desc', 'stop_lat', 'stop_lon']
	#print stops_dict[row[0]] # last one
	print('stops_dict loaded. stop count ', len(stops_dict))
	
	# >>> process loaded files
	
	train_routes_set = set([])
	for [route_id,agency_id] in routes_list :
		if agency_id == '2' : train_routes_set.add(route_id)
	#print train_routes_set
	
	train_trips_set = set([])
	for [route_id,trip_id] in trips_list :
		if route_id in train_routes_set : train_trips_set.add(trip_id)
	#print train_trips_set
	
	train_stops_set = set([])
	for [trip_id,stop_id] in stop_times_list :
		if trip_id in train_trips_set : train_stops_set.add(stop_id)
	print(train_stops_set)
	print('len(train_stops_set) : ', len(train_stops_set))
	
	train_stops_list = []
	for stop_id in train_stops_set :
		[stop_name, stop_desc, stop_lat, stop_lon] = stops_dict[stop_id]
		train_stops_list.append([stop_id, stop_name, stop_lat, stop_lon])
	
	# ************************************************************************************************************************
	# open and prep output txt file 
	#
	print('open file ', pathout+txtfileout)
	fileout = open(pathout+txtfileout, 'w', encoding="utf8") # save results in file
	postsline = 'stop_id,stop_name,stop_lat,stop_lon\n'
	print(postsline)
	fileout.write(postsline)
	outfilelinecount = 0
	
	for [stop_id, stop_name, stop_lat, stop_lon] in train_stops_list :
		if '/' in stop_name : stop_name = stop_name[:stop_name.find('/')]
		postsline = ','.join([stop_id, stop_name, str(stop_lat), str(stop_lon)])+'\n'
		fileout.write(postsline)
		outfilelinecount += 1
	fileout.close()
	print('close file ', pathout+txtfileout)
	print('lines in out file count ', outfilelinecount)
	
	# ************************************************************************************************************************
	# open and output js file 
	#
	print(("Saving file: " + gtfspathout+jsfileout+ " ..."))
	nf = open(gtfspathout+jsfileout, "w", encoding="utf8")
	outstr = 'var trainstopsName = {\n'
	for [stop_id, stop_name, stop_lat, stop_lon] in train_stops_list :
		nf.write(outstr)
		if '/' in stop_name : stop_name = stop_name[:stop_name.find('/')]
		outstr = stop_id+': "'+stop_name+'",\n'
	outstr = outstr[:-2]+'\n}'
	nf.write(outstr)
	nf.close()
	print(("Saved file: " + jsfileout))
	
	print("Local current time :", time.asctime( time.localtime(time.time()) ))

