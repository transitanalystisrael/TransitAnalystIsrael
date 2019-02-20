#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this file replaced GTFS_trips_at_time_and_shape__per_unique_route v3.py
#
# count the number of trips per day tpd for all lines (unique routes)
# in a GTFS file over the first week of the entire service period
# also collect set of stops per route and use to merge routes with same short name that share some stops
#
# inputs:
#   parent_path = 'C:\\transitanalyst\\processed\\'
#   gtfs_parant_path = 'C:\\transitanalyst\\gtfs\\'
#   gtfsdir = 'israel20181021'
#   sstarttime = '00:00:00'
#   sstoptime = '24:00:00'
#   FREQUENT_TPD = 60 # e.g. 8 tpd for delta time from start to stop of 2 hours is average of 4 trips an hour 
#   MIN_PERCENT_COMMON_STOPS = 10 # to be considered same line if also route short name (line number) is the same
#
# outputs:
#   txt file of routes with tripcount and stops count - 'routeswtripcountperday.txt'
#   txt file of unique routes - 'uniquerouteswtripcountat'+sstarttimename+sstoptimename+'.txt'
#   js file of routes with name max trips per day and shape geometry - 'route_freq_at'+sstarttimename+sstoptimename+'_'+sstartservicedate+'.js'
#   txt file for histogram of samestops for route_id pairs - samestopshist.txt
#
print '----------------- count the number of trips per day tpd for all lines (unique routes) --------------------------'
print 'generate js file of routes with name max trips per day and shape geometry'
from datetime import date
from datetime import timedelta
import time
import copy
import json
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
# scan lines in calendar to compute start and end service dates and to fill calendar_dict with calendar lines keyed on service_id
#
# create trips per day list with service day (from start to end) and count of 0 for tripsperday 
#   use as template for trips per day lists per route
#
# scan routes.txt to create a routes dict keyed on route_id that includes a route name, an empty set of trip_id s for this route and a 
# trips per day at route list with service day (from start to end) and count of 0, also set of stop_id s per route
#
# scan trips.txt to populate trip_id set per route in the routes dict
# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id
#
# scan routes dict to populate trips per day by looking up the each trip_id in the set in the trip dict
#   to get the service_id to look up the service days in the calendar dict
#   also update the total count
#
# scan stop_times.txt to populate stop_id set per route in the routes dict
# to find route_id - lookup trip_id in trips dict 
#
#_________________________________
#
parent_path = 'C:\\transitanalyst\\processed\\'
gtfs_parent_path = 'C:\\transitanalyst\\gtfs\\'
gtfsdir = 'israel20181021'

sstarttime = '00:00:00'
sstoptime = '24:00:00'
sstarttimename = '_'+sstarttime[0:2]+sstarttime[3:5]
sstoptimename = '-'+sstoptime[0:2]+sstoptime[3:5]

FREQUENT_TPD = 10 # e.g. 8 tpd for delta time from start to stop of 2 hours is average of 4 trips an hour 
MIN_PERCENT_COMMON_STOPS = 2 # to be considered same line if also route short name (line number) is the same

gtfspathin = gtfs_parent_path+gtfsdir+'\\'
gtfspath = gtfspathin
gtfspathout = parent_path
routeswithtripcountfile = 'routeswtripcountperday.txt'
uniquerouteswithtripcountattimefile = 'uniquerouteswtripcountat'+sstarttimename+sstoptimename+'.txt'

DAYSTOCOUNT = 7
daysofservicetocount = DAYSTOCOUNT - DAYSTOCOUNT/7

MAX_STOPS_COUNT = 50000
MAX_STOP_TIMES_COUNT = 25000000
MAX_TRIPS_COUNT = 900000
MAX_SHAPES_COUNT = 10000000
MAX_ROUTES_COUNT = 15000
MAX_AGENCY_COUNT = 100
MAX_CALENDAR_COUNT = 250000

#
# scan lines in calendar to compute start and end service dates and to fill calendar_dict with calendar lines keyed on service_id
#
maxfilelinecount = MAX_CALENDAR_COUNT
gtfsfile = 'calendar.txt'
inid = 'service_id'
calendar_dict = {}
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
service_id_i = keylist.index('service_id')
sunday_i = keylist.index('sunday')
monday_i = keylist.index('monday')
tuesday_i = keylist.index('tuesday')
wednesday_i = keylist.index('wednesday')
thursday_i = keylist.index('thursday')
friday_i = keylist.index('friday')
saturday_i = keylist.index('saturday')
start_date_i = keylist.index('start_date')
end_date_i = keylist.index('end_date')
calendar_dict = {keylist[inid_index]:slinelist}
#print calendar_dict
# scan lines in calendar 
count = 0
sstartservicedate = '25250101'
sendservicedate  = '15150101'
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	calendar_dict[slinelist[inid_index]] = slinelist
	sstartservicedate = min(sstartservicedate, slinelist[start_date_i])
	sendservicedate = max(sendservicedate, slinelist[end_date_i])
	#print calendarline_dict
	#print calendar_dict
	#print '------------------'
	count += 1
	sline = filein.readline()
print '------------------'
#print calendar_dict
print sstartservicedate, sendservicedate
filein.close()

#
# print int(sstartservicedate[0:4]),int(sstartservicedate[4:6]),int(sstartservicedate[6:8])
# from str to date format

startservicedate = date(int(sstartservicedate[0:4]),int(sstartservicedate[4:6]),int(sstartservicedate[6:8]))
endservicedate = date(int(sendservicedate[0:4]),int(sendservicedate[4:6]),int(sendservicedate[6:8]))
print 'startservicedate, endservicedate ', startservicedate, endservicedate

#
# create trips per day list with service day (from start to end) and count of 0 for tripsperday 
#   use as template for trips per day lists per route
#
tripsperdaylist = []
if (endservicedate.toordinal()-startservicedate.toordinal()) > DAYSTOCOUNT :  endservicedate = startservicedate + timedelta(days=DAYSTOCOUNT-1)
print 'startservicedate, endservicedate ', startservicedate, endservicedate
for ordservicedate in range (startservicedate.toordinal(), endservicedate.toordinal()+1):
	servicedate = date.fromordinal(ordservicedate)
	servicedayofweek = servicedate.weekday()
	print servicedate, servicedayofweek
	tripsperdaylist.append([servicedate, 0])
print '----tripsperdaylist----'
for [dayofservice, tripsperday] in tripsperdaylist:
	print dayofservice, tripsperday


#
# scan routes.txt to create a routes dict keyed on route_id that includes a route name, an empty set of trip_id s for this route and a 
# trips per day at route list with service day (from start to end) and count of 0, also set of stop_id s per route and a direction_id placeholder
#
maxfilelinecount = MAX_ROUTES_COUNT
gtfsfile = 'routes.txt'
inid = 'route_id'
routes_dict = {}
tripsperroute_set = set([]) # set of trip_id s of all trips that share the same route
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
route_id_i = keylist.index('route_id')
agency_id_i = keylist.index('agency_id')
route_short_name_i = keylist.index('route_short_name')
route_long_name_i = keylist.index('route_long_name')
route_desc_i = keylist.index('route_desc')
route_type_i = keylist.index('route_type')
#routes_dict = {keylist[inid_index]:[slinelist[agency_id_i], slinelist[route_short_name_i], slinelist[route_long_name_i], slinelist[route_desc_i], slinelist[route_type_i], set(['trip_id']), copy.deepcopy(tripsperdaylist), 0, set(['stop_id']), str(-1)]}
#print routes_dict
# scan gtfsfile
count = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	routes_dict[slinelist[inid_index]] = [slinelist[agency_id_i], slinelist[route_short_name_i], slinelist[route_long_name_i], slinelist[route_desc_i], slinelist[route_type_i], set([]), copy.deepcopy(tripsperdaylist), 0, set([]), str(-1)]
	count += 1
	sline = filein.readline()
print '------------------'
#print routes_dict
#for route_id, routesdictlist in routes_dict.iteritems():
#	print route_id, routesdictlist[:2], list(routesdictlist[2])
print '------------------'

print 'route lines scanned ', count 
filein.close()

#
# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id and shape_id and start_time placeholder and direction
# trips.txt : route_id,service_id,trip_id,trip_headsign,direction_id,shape_id

maxfilelinecount = MAX_TRIPS_COUNT
gtfspath = gtfspathin
gtfsfile = 'trips.txt'
inid = 'trip_id'
trips_dict = {}
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
trip_id_i = keylist.index('trip_id')
service_id_i = keylist.index('service_id')
route_id_i = keylist.index('route_id')
direction_id_i = keylist.index('direction_id')
shape_id_i = keylist.index('shape_id')
trips_dict = {keylist[inid_index]:[slinelist[service_id_i], slinelist[route_id_i], slinelist[shape_id_i], '00:00:00', slinelist[direction_id_i]]}
print trips_dict
# scan gtfsfile
count = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	trips_dict[in_id] = [slinelist[service_id_i], slinelist[route_id_i], slinelist[shape_id_i], '00:00:00', slinelist[direction_id_i]]
	count += 1
	if count < 5 : print in_id, trips_dict[in_id]
	sline = filein.readline()
print '------------------'
#print trips_dict
#for trip_id, tripsdictlist in trips_dict.iteritems():
#	print trip_id, tripsdictlist
print 'trips lines scanned ', count 
filein.close()

#
# scan stop_times.txt to populate trip start_time in trips dict
#
maxfilelinecount = MAX_STOP_TIMES_COUNT
gtfspath = gtfspathin
gtfsfile = 'stop_times.txt'
inid = 'stop_id'
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
stop_id_i = keylist.index('stop_id')
trip_id_i = keylist.index('trip_id')
departure_time_i = keylist.index('departure_time')
stop_sequence_i = keylist.index('stop_sequence')
# scan gtfsfile
count = 0
tripcount = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	stop_sequence = slinelist[stop_sequence_i]
	if stop_sequence == '1' :
		trip_id = slinelist[trip_id_i]
		trips_dict[trip_id][3] = slinelist[departure_time_i]
		tripcount += 1
		if tripcount < 5 : print trip_id, trips_dict[trip_id]
	count += 1
	sline = filein.readline()
print '------------------'
#print trips_dict
print 'stop_times lines scanned, tripcount ', count, tripcount
filein.close()

#
# scan trips.txt to populate trip_id set per route in the routes dict and direction_id into routes dict
#
maxfilelinecount = MAX_TRIPS_COUNT
gtfspath = gtfspathin
gtfsfile = 'trips.txt'
inid = 'route_id'
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
trip_id_i = keylist.index('trip_id')
direction_id_i = keylist.index('direction_id')
#service_id_i = keylist.index('service_id')
route_id_i = keylist.index('route_id')
trip_set_i = 5 #location of trip set in routes dict
direction_id_inroutesdict_i = 9 # location of direction_id in routes dict
#routes_dict[keylist[route_id_i]][trip_set_i].add(keylist[trip_id_i])
# scan gtfsfile
count = 0
tripscount = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	if routes_dict.has_key(slinelist[inid_index]):
		trip_id = slinelist[trip_id_i]
		direction_id = slinelist[direction_id_i]
		routes_dict[slinelist[inid_index]][trip_set_i].add(trip_id)
		direction_id_inroutesdict = routes_dict[slinelist[inid_index]][direction_id_inroutesdict_i]
		if direction_id_inroutesdict == str(-1) : # first time for this route_id in trips.txt
			routes_dict[slinelist[inid_index]][direction_id_inroutesdict_i] = direction_id
		else : # not first time make sure no change in direction for same route_id
			if direction_id_inroutesdict != direction_id : 
				print '************* ERROR *********** direction_id_inroutesdict != direction_id', direction_id_inroutesdict, direction_id
		tripscount += 1
	count += 1
	sline = filein.readline()
print '------------------'
#print routes_dict
#for route_id in routes_dict: print route_id, routes_dict[route_id][:2], list(routes_dict[route_id][trip_set_i])[0:2]
print 'trips lines scanned ', count
print 'trips added to routes dict ', tripscount 
filein.close()

#
# scan routes dict to populate trips per day by looking up the each trip_id in the set in the trip dict
#	filter by peak time the trips to count. look up the trip start_time in the trips dict
#   to get the service_id to look up the service days in the calendar dict
#   also update the total count
#
count = 0
tripcount = 0
dayofweek=[monday_i, tuesday_i, wednesday_i, thursday_i, friday_i, saturday_i, sunday_i]
maxtripsperdayanyroute = 0
maxtotaltripsanyroute = 0
for route_id, [agency_id,route_short_name,route_long_name,route_desc,route_type, tripset, tpdlist, totaltpdperroute, stopset, direction_id] in routes_dict.iteritems():
	#print route_id, agency_id,route_short_name,route_long_name,route_desc,route_type , list(tripset)[:2], tpdlist[:2], totaltripsperroute
	count += 1
	for trip_id in tripset:
		trip_start_time = trips_dict[trip_id][3]
		if trip_start_time >= sstarttime and trip_start_time < sstoptime : # if trip starts between sstarttime and sstoptime of requested period then count trips
			service_id = trips_dict[trip_id][0]
			slinelist = calendar_dict[service_id] # use service_id from trips_dict to look up calendar line list
			sstartcalendardate = slinelist[start_date_i]
			sendcalendardate = slinelist[end_date_i]
			startcalendardate = date(int(sstartcalendardate[0:4]),int(sstartcalendardate[4:6]),int(sstartcalendardate[6:8])) # start date for trip service
			endcalendardate = date(int(sendcalendardate[0:4]),int(sendcalendardate[4:6]),int(sendcalendardate[6:8])) # end date for trip service
			#print startcalendardate, endcalendardate, ' start and end date for trip service'
			#print startservicedate, endservicedate, ' start and end date for all service'
			for ordcalendardate in range(max(startcalendardate.toordinal(),startservicedate.toordinal()),min(endcalendardate.toordinal(),endservicedate.toordinal())+1):
				calendardate = date.fromordinal(ordcalendardate)
				calendardayofweek = calendardate.weekday()
				#print calendardate, calendardayofweek, slinelist[dayofweek[calendardayofweek]]
				if tpdlist[(calendardate-startservicedate).days][0] != calendardate :
					print '******error**************'
					print tpdlist[(calendardate-startservicedate).days][0], calendardate 
				tpdlist[(calendardate-startservicedate).days][1] += int(slinelist[dayofweek[calendardayofweek]]) # add to trip count for that day
	totaltripsperroute = 0
	maxtripsperdayperroute = 0
	for [dayofservice, trips] in tpdlist: # scan all service days per stop to accumulate total trips at stop from trips per day at stop
		maxtripsperdayperroute = max(maxtripsperdayperroute, trips)
		totaltripsperroute += trips # and add to total trips at stop
	routes_dict[route_id][7] = totaltripsperroute
	maxtotaltripsanyroute = max(maxtotaltripsanyroute, totaltripsperroute)
	#print route_id, agency_id,route_short_name,route_long_name,route_desc,route_type , list(tripset)[:2], tpdlist[:2], totaltripsperroute
	if totaltripsperroute>= maxtotaltripsanyroute : print route_id, agency_id, route_short_name, totaltripsperroute
	#if totaltripsperroute>1000 : print route_id, agency_id,route_short_name,route_long_name,route_desc,route_type , list(tripset)[:2], tpdlist, totaltripsperroute
	#print 'maxtripsperdayperroute ', maxtripsperdayperroute
	#print 'maxtotaltripsanyroute ', maxtotaltripsanyroute
print 'count ', count
print 'maxtotaltripsanyroute ', maxtotaltripsanyroute

#
# scan stop_times.txt to populate stop_id set per route in the routes dict
# to find route_id - lookup trip_id in trips dict 
#
maxfilelinecount = MAX_STOP_TIMES_COUNT
gtfspath = gtfspathin
gtfsfile = 'stop_times.txt'
inid = 'stop_id'
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
stop_id_i = keylist.index('stop_id')
trip_id_i = keylist.index('trip_id')
stop_set_i = 8;
#routes_dict = {route_id:[agency_id, route_short_name, route_long_name, route_desc, route_type, set(['trip_id']), copy.deepcopy(tripsperdaylist), 0, set(['stop_id']), direction_id]}
# scan gtfsfile
count = 0
stopscount = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	stop_id = slinelist[stop_id_i]
	trip_id = slinelist[trip_id_i]
	route_id = trips_dict[trip_id][1]
	routes_dict[route_id][stop_set_i].add(stop_id)
	count += 1
	sline = filein.readline()
print '------------------'
#print routes_dict
print 'stop_times lines scanned ', count
filein.close()

#
# output to file of routes with tripcount and stops count
#  while we are at it - collect the set of route_id s of routes with zero total trips per route for later cleanup
#
fileout = open(gtfspathout+routeswithtripcountfile, 'w') # save results in file
postsline = 'route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,totaltripsperroute,'
postsline += 'day1,tpd1,day2,tpd2,day3,tpd3,day4,tpd4,day5,tpd5,day6,tpd6,day7,tpd7,stopsperroute,direction_id\n'
fileout.write(postsline)
routeswnotripsset = set()
for route_id, [agency_id,route_short_name,route_long_name,route_desc,route_type, tripset, tpdlist, totaltpdperroute, stopset, direction_id] in routes_dict.iteritems():
	if totaltpdperroute == 0 : routeswnotripsset.add(route_id)
	postsline = route_id+','+agency_id+','+route_short_name+','+route_long_name+','+route_desc+','+route_type+','+str(totaltpdperroute)
	for [dayofservice, trips] in tpdlist: # scan all service days per route 
		postsline += ','+str(dayofservice)+','+str(trips)
	postsline += ','+str(len(stopset))
	postsline += ','+str(direction_id)
	postsline += '\n'
	fileout.write(postsline)
fileout.close()
print gtfspathout+routeswithtripcountfile
print 'count ', count
print 'maxtotaltripsanyroute ', maxtotaltripsanyroute
#print 'routeswnotripsset - ', routeswnotripsset

#
# clean up routes_dict by removing routes in the routeswnotripsset - they have tripcount of zero
#
for route_id in routeswnotripsset : del routes_dict[route_id]

#
# scan shapes.txt to create shape dict keyed on shape_id and includes list of latlon points
#
maxfilelinecount = MAX_SHAPES_COUNT
gtfspath = gtfspathin
gtfsfile = 'shapes.txt'
inid = 'shape_id'
shapes_dict = {}
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
shape_id_i = keylist.index('shape_id')
shape_pt_lat_i = keylist.index('shape_pt_lat')
shape_pt_lon_i = keylist.index('shape_pt_lon')
shape_pt_sequence_i = keylist.index('shape_pt_sequence')
# scan gtfsfile
count = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id 
	if in_id in shapes_dict :
		shapes_dict[in_id].append([slinelist[shape_pt_lat_i], slinelist[shape_pt_lon_i], slinelist[shape_pt_sequence_i]])
	else: # first one
		shapes_dict[in_id] = [[slinelist[shape_pt_lat_i], slinelist[shape_pt_lon_i], slinelist[shape_pt_sequence_i]]]
	count += 1
	sline = filein.readline()
print '------------------'
#print shapes_dict['62440']
print 'shapes lines scanned ', count 
filein.close()
#
# order shapes in shape dict using pt sequence number
#
#print shapes_dict['64254'][:10]
for shape_id, shape_pt_list in shapes_dict.iteritems() :
	shape_pt_list.sort(key=lambda shape_pt: int(shape_pt[2]))
#print shapes_dict['64254'][:10]
#	
# create routes dict with shape_id and with max trips per day 
#
routeswshape_dict = {}
for route_id, [agency_id,route_short_name,route_long_name,route_desc,route_type, tripset, tpdlist, totaltpdperroute, stopset, direction_id] in routes_dict.iteritems():
	#print 'route_id,agency_id,route_short_name,totaltpdperroute ', route_id,agency_id,route_short_name,totaltpdperroute 
	#print 'routes_dict[route_id] ', routes_dict[route_id]
	shape_id = trips_dict[tripset.pop()][2] # random trip... would be good to check that same stops trips have same shape and to select the best trip shape from similar route_ids
	if shape_id == '' : 
		print 'agency_id,route_short_name,', agency_id,route_short_name
		print "trips_dict[in_id] = [service_id, route_id, shape_id, '00:00:00', direction_id]"
		for trip_id in tripset : 
			print 'shapes for tripset ', trips_dict[trip_id]
	#tpds = []
	#for [day,tpd] in tpdlist: tpds.append(tpd)
	#maxtpdperroute = max(tpds)
	maxtpdperroute = 0
	for [dayofservice, trips] in tpdlist: # scan all service days per route 
		maxtpdperroute = max(maxtpdperroute, trips)
	routeswshape_dict[route_id] = [agency_id,route_short_name,totaltpdperroute,maxtpdperroute,shape_id]
	#print 'route_id, shape_id ', route_id, shape_id


#for route_id, [agency_id,route_short_name,totaltpdperroute,maxtpdperroute,shape_id] in routeswshape_dict.iteritems():
	#print 'route_id, totaltpdperroute, maxtpdperroute, shape_id ', route_id, totaltpdperroute, maxtpdperroute, shape_id
	#print 'route_id, totaltpdperroute, tpdlist ', route_id, routes_dict[route_id][7], routes_dict[route_id][6]

#
# scan agency.txt to create agency dict keyed on agency_id and includes agency name
#
maxfilelinecount = MAX_AGENCY_COUNT
gtfspath = gtfspathin
gtfsfile = 'agency.txt'
inid = 'agency_id'
agency_dict = {}
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
agency_id_i = keylist.index('agency_id')
agency_name_i = keylist.index('agency_name')
# scan gtfsfile
count = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id 
	agency_dict[in_id] = slinelist[agency_name_i]
	count += 1
	sline = filein.readline()
print '------------------'
#print agency_dict
print 'agency lines scanned ', count 
filein.close()

#
# output to file of unique routes and create list of unique routes that are frequent and dict of unique routes that are frequent
#
def addtpd(x, y): return [x[0],x[1]+y[1]]
count=0
merge_count=0
unique_route_id_list = []
unique_route_dict = {}
same_stops = False
used_route_id_set = set()
fileout = open(gtfspathout+uniquerouteswithtripcountattimefile, 'w') # save results in file
fileouthist = open(gtfspathout+'samestopshist.txt', 'w') # save results in file
#postsline = 'route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,totaltripsperroute,'
#postsline += 'day1,tpd1,day2,tpd2,day3,tpd3,day4,tpd4,day5,tpd5,day6,tpd6,day7,tpd7\n'
postsline = 'route_id,agency_id,route_short_name,totaltripsperroute,'
postsline += 'maxtpdperroute,'
postsline += 'shape_id'
postsline += '\n'
fileout.write(postsline)
postslinehist = 'routeid1,routeid2,percent_common_stops,stops1,stops2\n'
fileouthist.write(postslinehist)
print postsline
for route_id, [agency_id,route_short_name,route_long_name,route_desc,route_type, tripset, tpdlist, totaltpdperroute, stopset, direction_id] in routes_dict.iteritems():
	count += 1
	#print 'route count ', count
	if route_id not in used_route_id_set :
		out_route_list = [route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,tpdlist,totaltpdperroute]
		#out_route_list = [route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,tpdlist,totaltpdperroute,route_id] # debug
		used_route_id_set.add(route_id)
		for route_id2, [agency_id2,route_short_name2,route_long_name2,route_desc2,route_type2, tripset2, tpdlist2, totaltpdperroute2, stopset2, direction_id2] in routes_dict.iteritems():
			common_stop_set = stopset & stopset2
			percent_common_stops = 100*len(common_stop_set)/max(len(stopset),len(stopset2))
			same_stops = len(common_stop_set) == len(stopset) and len(stopset) == len(stopset2)
			same_or_similar = same_stops or (percent_common_stops > MIN_PERCENT_COMMON_STOPS and route_short_name == route_short_name2 and agency_id == agency_id2 and direction_id == direction_id2 and agency_id != '2') # Not train!!!
			
			
			
			same_or_similar_for_histo = same_stops or (percent_common_stops > 0 and route_short_name == route_short_name2 and agency_id == agency_id2 and direction_id == direction_id2 and agency_id != '2') # Not train!!!
			if same_or_similar_for_histo and (route_id != route_id2) and (route_id2 not in used_route_id_set) :
				#print route_id, route_id2, percent_common_stops
				postslinehist = route_id+','+route_id2+','+str(percent_common_stops)+','+str(len(stopset))+','+str(len(stopset2))+'\n'
				fileouthist.write(postslinehist)
			
			
			
			
			if same_or_similar and (route_id != route_id2) and (route_id2 not in used_route_id_set) : # same stops or (similar stops and same name) for both routes and not same route_id
				# merge the two routes
				merge_count += 1
				#print out_route_list[0]
				route_list2 = [route_id2,agency_id2,route_short_name2,route_long_name2,route_desc2,route_type2,tpdlist2,totaltpdperroute2]
				#print route_list2[0]
				#out_route_list = [out_route_list[0],agency_id,route_short_name,route_long_name,route_desc,route_type,map(addtpd,out_route_list[6],tpdlist2),out_route_list[7]+totaltpdperroute2,out_route_list[8]+'_'+route_id2]  # debug
				out_route_list = [out_route_list[0],agency_id,route_short_name,route_long_name,route_desc,route_type,map(addtpd,out_route_list[6],tpdlist2),out_route_list[7]+totaltpdperroute2]
				#print out_route_list[0]
				used_route_id_set.add(route_id2)
		postsline = out_route_list[0]+','+out_route_list[1]+','+out_route_list[2]+','+str(out_route_list[7])
		totaltpd = out_route_list[7]
		maxtpd = 0
		for [dayofservice, trips] in out_route_list[6]: # scan all service days per route  = 
			#postsline += ','+str(dayofservice)+','+str(trips)
			maxtpd = max(maxtpd, trips)
		postsline += ','+str(maxtpd)
		postsline += ','+routeswshape_dict[route_id][4]
		#postsline += out_route_list[8] # debug
		postsline += '\n'
		fileout.write(postsline)
		# append to list only if frequent route: FREQUENT_TPD or more trips from start time to stop time. filter out singular events during the week like lag-ba-omer
		if maxtpd >= FREQUENT_TPD and totaltpd > maxtpd*daysofservicetocount/2: 
			unique_route_id_list.append(out_route_list[0]) 
			unique_route_dict[out_route_list[0]] = [out_route_list[1],out_route_list[2],out_route_list[7],maxtpd]

		if maxtpd >= FREQUENT_TPD and totaltpd <= maxtpd*daysofservicetocount/2: print "filtered out :", postsline

fileout.close()
fileouthist.close()
print gtfspathout+uniquerouteswithtripcountattimefile
print 'count, merge_count, unique:  ', count, merge_count, len(unique_route_id_list)
print unique_route_id_list[:10]

#
# output geojson file of routes with name max trips per day and shape geometry
#

def getJSON(r_id):
	#print r_id
	#print shapes_dict['64254'][:3]
	#print routeswshape_dict[r_id]
	#print routeswshape_dict[r_id][4]
	#print shapes_dict[routeswshape_dict[r_id][4]][:3]
	if routeswshape_dict[r_id][4] == '' : # no shape defined
		print '************************ no shape defined ****************************************************** using dummy'
		return {
			"type": "Feature",
			"geometry": {
				"type": "LineString",
				"coordinates": [[float('35.094763'), float('32.989482')],[float('35.105822'), float('33.023624')]] # dummy shape - need to replace with stop location sequence
			},
			"properties": { # agency_id,route_short_name,averagetpdperroute,maxtpdperroute
				"agency_id": unique_route_dict[r_id][0],
				"agency_name": agency_dict[unique_route_dict[r_id][0]],
				"route_short_name": unique_route_dict[r_id][1],
				"averagetpdperroute": unique_route_dict[r_id][2]/daysofservicetocount,
				"maxtpdperroute": unique_route_dict[r_id][3]
			}
		}
	else: # shape defined
		return {
			"type": "Feature",
			"geometry": {
				"type": "LineString",
				"coordinates": [[round(float(shape_pt_lon),5), round(float(shape_pt_lat),5)] for [shape_pt_lat, shape_pt_lon, shape_pt_sequence] in shapes_dict[routeswshape_dict[r_id][4]]] # shape_id_i = 4
			},
			"properties": { # agency_id,route_short_name,averagetpdperroute,maxtpdperroute
				"agency_id": unique_route_dict[r_id][0],
				"agency_name": agency_dict[unique_route_dict[r_id][0]],
				"route_short_name": unique_route_dict[r_id][1],
				"averagetpdperroute": unique_route_dict[r_id][2]/daysofservicetocount,
				"maxtpdperroute": unique_route_dict[r_id][3]
			}
		}

# saveGeoJSON
jsfileout = 'route_freq_at'+sstarttimename+sstoptimename+'_'+sstartservicedate+'.js'
print ("Generating GeoJSON export.")
geoj = {
	"type": "FeatureCollection",
	"features": [getJSON(route_id) for route_id in unique_route_id_list]
}

print ("Saving file: " + gtfspathout+jsfileout+ " ...")
nf = open(gtfspathout+jsfileout, "w")
jsonstr = json.dumps(geoj, separators=(',',':')) # smaller file for download
outstr = jsonstr.replace('}},', '}},\n')
nf.write('var freqRoutes =\n')
nf.write(outstr)
nf.close()
print ("Saved file: " + jsfileout)
