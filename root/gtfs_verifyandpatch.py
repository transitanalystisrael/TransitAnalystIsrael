#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# check GTFS files for inconsistencies and try to patch them with minimal changes
# e.g. a trip that references a route_id that does not exist in routes.txt (found in GTFS Israel file with start service date of 21 March 2019)
#
# most of the patches are now only placeholders... need to add...
# need to rerun after patch to see that nothing was broken by fix... this is not done yet
#
import time
import csv
from pathlib import Path

cwd = Path.cwd()
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
	# input:
	parent_path = cwd.parent / gtfsparentpath
	gtfsdir = gtfsdirbase+gtfsdate
	txtfilein = ''
	
	# output:
	gtfspathout = cwd.parent / pathout / gtfsdir
	txtfileout = ''
	
	gtfspathin = parent_path / gtfsdir
	gtfspath = gtfspathin
	
	# >>> load routes file
	txtfilein = 'routes.txt'
	routes_dict = {}
	with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # [route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_color]
		#print(header)
		for row in reader:
			#print row
			routes_dict[row[0]] = [row[1]] # 'route_id' : ['agency_id']
	#print routes_dict[:4]
	print('routes_dict loaded. routes count ', len(routes_dict))
	
	# >>> load trips file
	txtfilein = 'trips.txt'
	trips_dict = {}
	with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
		#print(header)
		for row in reader:
			#print row
			trips_dict[row[2]] = [row[0],row[1],row[5]] # 'trip_id' : ['route_id','service_id','shape_id']
	#print trips_dict[:4]
	print('trips_dict loaded. trips count ', len(trips_dict))
	
	# >>> load stop_times file
	txtfilein = 'stop_times.txt'
	stop_times_trips_set = set([])
	stop_times_stops_set = set([])
	with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # [trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled]
		#print(header)
		for row in reader:
			#print row
			stop_times_trips_set.add(row[0]) # trip_id
			stop_times_stops_set.add(row[3]) # stop_id
	print('stop_times_trips loaded. trips count ', len(stop_times_trips_set))
	print('stop_times_stops loaded. stops count ', len(stop_times_stops_set))
	
	# >>> load stops file
	txtfilein = 'stops.txt'
	stops_dict = {}
	with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'zone_id']
		#print(header)
		for row in reader:
			#print row
			stops_dict[row[0]] = [row[2], row[3], row[4], row[5]] # 'stop_id' : ['stop_name', 'stop_desc', 'stop_lat', 'stop_lon']
	#print stops_dict[row[0]] # last one
	print('stops_dict loaded. stop count ', len(stops_dict))
	
	# >>> load agency file
	txtfilein = 'agency.txt'
	agency_dict = {}
	with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url
		#print(header)
		for row in reader:
			#print row
			agency_dict[row[0]] = [row[1]] # 'agency_id' : ['agency_name']
	#print agency_dict[row[0]] # last one
	print('agency_dict loaded. agency count ', len(agency_dict))
	
	# >>> load shapes file. Actually loads only one point per shape!!! used only as a set of shape_ids
	txtfilein = 'shapes.txt'
	shapes_dict = {}
	with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
		#print(header)
		for row in reader:
			#print row
			shapes_dict[row[0]] = [row[1], row[2]] # 'shape_id' : ['shape_pt_lat','shape_pt_lon']
	#print shapes_dict[row[0]] # last one
	print('shapes_dict loaded. shape count ', len(shapes_dict))
	
	# >>> load calendar file
	txtfilein = 'calendar.txt'
	calendar_dict = {}
	with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # service_id,sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date
		#print(header)
		for row in reader:
			#print row
			calendar_dict[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]] # ['service_id' : [ 'sunday','monday','tuesday','wednesday','thursday','friday','saturday','start_date','end_date']
	#print calendar_dict[row[0]] # last one
	print('calendar_dict loaded. calendar count ', len(calendar_dict))
	
	
	# >>> process loaded files
	
	
	# >>> process routes
	routes_agency_id_ok_count = 0
	routes_agency_id_problem_count = 0
	routes_agency_id_problem_list = []
	for route_id, [agency_id] in routes_dict.items() :
		if agency_id in agency_dict :
			routes_agency_id_ok_count +=1
		else :
			routes_agency_id_problem_count +=1
			print('routes_agency_id_problem : ', route_id, agency_id)
			routes_agency_id_problem_list.append(route_id)
	print('routes_agency_id_ok_count : ', routes_agency_id_ok_count)
	print('routes_agency_id_problem_count : ', routes_agency_id_problem_count)
	
	# >>> process trips
	trips_service_id_ok_count = 0
	trips_service_id_problem_count = 0
	trips_service_id_problem_list = []
	trips_shape_id_ok_count = 0
	trips_shape_id_problem_count = 0
	trips_shape_id_problem_list = []
	trips_route_id_ok_count = 0
	trips_route_id_problem_count = 0
	trips_route_id_problem_list = []
	for trip_id, [route_id,service_id,shape_id] in trips_dict.items() :
		if route_id in routes_dict :
			trips_route_id_ok_count +=1
		else :
			trips_route_id_problem_count +=1
			print('trips_route_id_problem : ', trip_id, route_id)
			trips_route_id_problem_list.append(trip_id)
		if shape_id in shapes_dict :
			trips_shape_id_ok_count +=1
		else :
			trips_shape_id_problem_count +=1
			print('trips_shape_id_problem : ', trip_id, shape_id)
			trips_shape_id_problem_list.append(trip_id)
		if service_id in calendar_dict :
			trips_service_id_ok_count +=1
		else :
			trips_service_id_problem_count +=1
			print('trips_service_id_problem : ', trip_id, service_id)
			trips_service_id_problem_list.append(trip_id)
	print('trips_service_id_ok_count : ', trips_service_id_ok_count)
	print('trips_service_id_problem_count : ', trips_service_id_problem_count)
	print('trips_shape_id_ok_count : ', trips_shape_id_ok_count)
	print('trips_shape_id_problem_count : ', trips_shape_id_problem_count)
	print('trips_route_id_ok_count : ', trips_route_id_ok_count)
	print('trips_route_id_problem_count : ', trips_route_id_problem_count)
	
	# >>> process stop_times
	stoptimes_trip_id_ok_count = 0
	stoptimes_trip_id_problem_count = 0
	stoptimes_trip_id_problem_list = []
	stoptimes_stop_id_ok_count = 0
	stoptimes_stop_id_problem_count = 0
	stoptimes_stop_id_problem_list = []
	for trip_id in stop_times_trips_set :
		if trip_id in trips_dict :
			stoptimes_trip_id_ok_count +=1
		else :
			stoptimes_trip_id_problem_count +=1
			print('stoptimes_trip_id_problem : ', trip_id)
			stoptimes_trip_id_problem_list.append(trip_id)
	for stop_id in stop_times_stops_set :
		if stop_id in stops_dict :
			stoptimes_stop_id_ok_count +=1
		else :
			stoptimes_stop_id_problem_count +=1
			print('stoptimes_stop_id_problem : ', stop_id)
			stoptimes_stop_id_problem_list.append(stop_id)
	print('stoptimes_trip_id_ok_count : ', stoptimes_trip_id_ok_count)
	print('stoptimes_trip_id_problem_count : ', stoptimes_trip_id_problem_count)
	print('stoptimes_stop_id_ok_count : ', stoptimes_stop_id_ok_count)
	print('stoptimes_stop_id_problem_count : ', stoptimes_stop_id_problem_count)
			
	
	# >>> patch problem files
	
	if routes_agency_id_problem_count != 0 :
		print('routes_agency_id_problem_count : ', routes_agency_id_problem_count)
		# erase routes if agency_id referenced is missing from agency.txt or add unknown agency to agency.txt with the missing id...
		# for now leaving as is
	
	if trips_service_id_problem_count != 0 :
		print('trips_service_id_problem_count : ', trips_service_id_problem_count)
		# erase trips if service_id referenced is missing from calendar.txt or add empty service record to calendar.txt with the missing id...
		# for now leaving as is
	
	if trips_shape_id_problem_count != 0 :
		print('trips_shape_id_problem_count : ', trips_shape_id_problem_count)
		# if shape_id == "" then create shape from sequence of stops and add to shapes.txt with the newly created id...
		# for now leaving as is
	
	if trips_route_id_problem_count != 0 :
		print('trips_route_id_problem_count : ', trips_route_id_problem_count)
		# erase trips if route_id referenced is missing from routes.txt or add unknown route to route.txt with the missing id...
		# for now doing the first - but checking that the erased trip will not be missed
		# load full trips.txt file  then apply the patch while writing back.
		
		# >>> load trips file
		txtfilein = 'trips.txt'
		trips_full_list = []
		with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
			reader = csv.reader(f)
			header = next(reader) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
			#print(header)
			for row in reader:
				#print row
				trips_full_list.append([row[0],row[1],row[2],row[3],row[4],row[5]]) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
		print('trips_full_list loaded. trips count ', len(trips_full_list))
		
		# >>> open and prep output txt file 
		txtfileout = 'trips.txt'
		print('open file ', gtfspathout / txtfileout)
		fileout = open(gtfspathout / txtfileout, 'w', encoding="utf8") # save results in file
		postsline = 'route_id,service_id,trip_id,trip_headsign,direction_id,shape_id\n'
		print(postsline)
		fileout.write(postsline)
		outfilelinecount = 0
		for [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id] in trips_full_list :
			if trip_id in trips_route_id_problem_list :
				print('trips_route_id_problem : ', trip_id, route_id)
				print('erasing trip_id from trips.txt')
				# check if this trip that we are erasing will be missed
				if trip_id in stop_times_trips_set :
					print('ooops **************** erased a trip that is referenced in stoptimes.txt : ', trip_id)
			else :
				postsline = ','.join([route_id,service_id,trip_id,trip_headsign,direction_id,shape_id])+'\n'
				fileout.write(postsline)
				outfilelinecount += 1
		fileout.close()
		print('close file ', gtfspathout / txtfileout)
		print('lines in out file count ', outfilelinecount)

	if stoptimes_trip_id_problem_count != 0 :
		print('stoptimes_trip_id_problem_count : ', stoptimes_trip_id_problem_count)
		# erase stoptimes if trip_id referenced is missing from trips.txt
		# for now leaving as is
		
	if stoptimes_stop_id_problem_count != 0 :
		print('stoptimes_stop_id_problem_count : ', stoptimes_stop_id_problem_count)
		# erase stoptimes if stop_id referenced is missing from stops.txt
		# for now leaving as is
	
