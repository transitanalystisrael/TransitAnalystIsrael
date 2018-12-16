#!/usr/bin/env python
# -*- coding: utf-8 -*-
# collect a set of trip_id s at all stops
# in a GTFS file over the selected week of the service period starting at serviceweekstartdate
#
# inputs:
#   parent_path = 'C:\\transitanalyst\\gtfs\\'
#   pathout = 'C:\\transitanalyst\\processed\\'
#   sserviceweekstartdate = '20181021'
#   gtfsdate = '20181021'
#   gtfsdir = 'israel'+gtfsdate
#   stopsneartrainstop_post_edit = 'stopsneartrainstop_post_edit'+'_'+servicedate+'.txt'
#
# outputs:
#   output txt file of stops with trip_id s -'stops_w_trip_ids'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#   output txt file of stops with trips per hour in day summed over one week -'stops_w_tph_summed_over_week'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#   output txtfileout3 of trainstops with trips per hour in day summed over one week -'trainstops_w_tph_summed_over_week'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#
print '----------------- collect a set of trip_id s at all stops --------------------------'
print 'output txt file of stops with trip_id s'
from datetime import date
from datetime import timedelta
import time
import copy
import json
import csv
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
# input:
parent_path = 'C:\\transitanalyst\\gtfs\\'
pathout = 'C:\\transitanalyst\\processed\\'
sserviceweekstartdate = '20181021' # recommend to use gtfsdate (expect gtfs files to be most accurate for first week in service range)
gtfsdate = '20181021'
gtfsdir = 'israel'+gtfsdate
servicedate = sserviceweekstartdate
stopsneartrainstop_post_edit = 'stopsneartrainstop_post_edit'+'_'+servicedate+'.txt'

# output:
txtfileout1 = 'stops_w_trip_ids'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
txtfileout2 = 'stops_w_tph_summed_over_week'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt' #  stops with trips per hour in day summed over one week 
txtfileout3 = 'trainstops_w_tph_summed_over_week'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt' # trainstops with trips per hour in day summed over one week 

#parent_path = 'C:\\transitanalyst\\processed\\' # small files for test
#gtfsdir = 'israel20180106-binyamina_station' # small files for test

gtfspathin = parent_path+gtfsdir+'\\'
gtfspath = gtfspathin
gtfspathout = pathout
processedpathin = pathout

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
print slinelist
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
dayofweek=[monday_i, tuesday_i, wednesday_i, thursday_i, friday_i, saturday_i, sunday_i]
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
serviceweekstartdate = date(int(sserviceweekstartdate[0:4]),int(sserviceweekstartdate[4:6]),int(sserviceweekstartdate[6:8]))
print 'startservicedate, endservicedate, serviceweekstartdate ', startservicedate, endservicedate, serviceweekstartdate

#
# create trips per hour list with hours from 0-30 (for times after midnight) and count of 0, for tripsperhour
#   use as template for trips per hour lists per stop 
#

dateinservicerange = lambda d: d >= startservicedate and d <= endservicedate

# print timedelta(days=1)
serviceweekenddate = serviceweekstartdate + timedelta(days=DAYSTOCOUNT-1)
print 'serviceweekstartdate, serviceweekenddate ', serviceweekstartdate, serviceweekenddate
if dateinservicerange(serviceweekstartdate) and dateinservicerange(serviceweekenddate) :
	print 'serviceweek selected is in service range' 
else :
	print 'error*********************serviceweek selected is NOT in service range: ' , serviceweekstartdate, serviceweekenddate, startservicedate, endservicedate
	exit()

print 'startservicedate, endservicedate ', startservicedate, endservicedate
startservicedate = serviceweekstartdate
endservicedate = serviceweekenddate
print 'startservicedate, endservicedate ', startservicedate, endservicedate

tripsperhourlist = []
for houratstop in range (31):
	tripsperhourlist.append(0)
print '----tripsperhourlist----'
print tripsperhourlist

#
# scan stops.txt to create a stops dict keyed on stop_id that includes lat lon, an empty dict of trip_id s and times at stop for this stop and a 
# trips per hour at stop list 
#   also calculate min and max lat lon#
maxfilelinecount = MAX_STOPS_COUNT
gtfsfile = 'stops.txt'
inid = 'stop_id'
stops_dict = {}
tripsperstop_dict = {} # dict of trip_id s and times at stop for this stop
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
inid_index = keylist.index(inid)
stop_id_i = keylist.index('stop_id')
stop_lat_i = keylist.index('stop_lat')
stop_lon_i = keylist.index('stop_lon')
stop_desc_i = keylist.index('stop_desc')
#stops_dict = {keylist[inid_index]:[slinelist[slinelist[stop_lat_i], slinelist[stop_lon_i], copy.deepcopy(tripsperstop_dict), copy.deepcopy(tripsperhourlist), 0]}
#print stops_dict
# scan gtfsfile
count = 0
minlat = '90.000000'
minlon = '90.000000'
maxlat = '00.000000'
maxlon = '00.000000'
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	stops_dict[slinelist[inid_index]] = [slinelist[stop_lat_i], slinelist[stop_lon_i], copy.deepcopy(tripsperstop_dict), copy.deepcopy(tripsperhourlist), 0]
	minlat = min(minlat, slinelist[stop_lat_i])
	maxlat = max(maxlat, slinelist[stop_lat_i])
	minlon = min(minlon, slinelist[stop_lon_i])
	maxlon = max(maxlon, slinelist[stop_lon_i])
	count += 1
	sline = filein.readline()
print '------------------'
#print stops_dict
#for stop_id, stopsdictlist in stops_dict.iteritems():
#	print stop_id, stopsdictlist[:2], list(stopsdictlist[2])
print '------------------'
print 'minlat, minlon : ', minlat, minlon
print 'maxlat, maxlon : ', maxlat, maxlon
print 'stop lines scanned ', count 
filein.close()

#
# scan stop_times.txt to populate trip_id dict per stop in the stops dict
#
maxtimeatstop = '00:00:00'
maxfilelinecount = MAX_STOP_TIMES_COUNT
gtfspath = gtfspathin
gtfsfile = 'stop_times.txt'
slinelist=[]
print gtfspath+gtfsfile
filein = open(gtfspath+gtfsfile, 'r')
sline = filein.readline()
slinelist=sline[:-1].split(",")
# print slinelist
keylist = slinelist
stop_id_i = keylist.index('stop_id') # index in stop_times slinelist.
trip_id_i = keylist.index('trip_id') # index in stop_times slinelist.
departure_time_i = keylist.index('departure_time') # index in stop_times slinelist.
trip_dict_i = 2; # index in stops_dict. changed from 2 when stop_desc added. changed back to 2 when desc removed 
# scan gtfsfile
count = 0
stopscount = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	stop_id = slinelist[stop_id_i]
	#print stop_id
	trip_id = slinelist[trip_id_i]
	departure_time = slinelist[departure_time_i]
	if stops_dict.has_key(stop_id):
		#print stop_id, trip_id, stops_dict[stop_id], stops_dict[stop_id][trip_dict_i]
		if stops_dict[stop_id][trip_dict_i].has_key(trip_id): # trip at stop more than once... yes it does happen
			stops_dict[stop_id][trip_dict_i][trip_id].append(departure_time)
			#print 'trips at stop more than once - ', stop_id, len(stops_dict[stop_id][trip_dict_i]), len(stops_dict[stop_id][trip_dict_i][trip_id])
		else : # trip at stop first time
			stops_dict[stop_id][trip_dict_i][trip_id] = [departure_time]
			#print 'trip at stop first time ********************** ', stop_id, stops_dict[stop_id][trip_dict_i]
		stopscount += 1
	else :
		print '************* error ** stop_id not found in stops_dict  ', stop_id
	count += 1
	maxtimeatstop = max(maxtimeatstop, departure_time)
	sline = filein.readline()
print '------------------'
#print stops_dict
#for stop_id in stops_dict: 
#	print stop_id, len(stops_dict[stop_id][trip_dict_i])
#	for trip_id in stops_dict[stop_id][trip_dict_i]:
#		print '>>>', trip_id, len(stops_dict[stop_id][trip_dict_i][trip_id])
#		if len(stops_dict[stop_id][trip_dict_i][trip_id]) > 1 : print '>>>>>>>>>>>>>>>>>>>>>>>>>>'
#print 'last stops_dict entry updated: ', stops_dict[slinelist[inid_index]]
print 'stop_times lines scanned ', count
print 'stops found in dict ', stopscount 
print 'maxlat, maxlon', maxlat, maxlon
print 'maxtimeatstop : ', maxtimeatstop
filein.close()

#
# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id and number of times the trip runs during the analyzed service week
#
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
trips_dict = {keylist[inid_index]:[slinelist[service_id_i], slinelist[route_id_i]]}
print trips_dict
# scan gtfsfile
count = 0
count_trip_ids_in_week = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	xinweek = 0
	service_id = slinelist[service_id_i]
	calslinelist = calendar_dict[service_id] # use service_id from trips_dict to look up calendar line list
	sstartcalendardate = calslinelist[start_date_i] # string
	sendcalendardate = calslinelist[end_date_i] # string
	startcalendardate = date(int(sstartcalendardate[0:4]),int(sstartcalendardate[4:6]),int(sstartcalendardate[6:8])) # start date for trip service
	endcalendardate = date(int(sendcalendardate[0:4]),int(sendcalendardate[4:6]),int(sendcalendardate[6:8])) # end date for trip service
	#print startcalendardate, endcalendardate, ' start and end date for trip service'
	#print startservicedate, endservicedate, ' start and end date for all service'
	for ordcalendardate in range(max(startcalendardate.toordinal(),startservicedate.toordinal()),min(endcalendardate.toordinal(),endservicedate.toordinal())+1):
		calendardate = date.fromordinal(ordcalendardate)
		calendardayofweek = calendardate.weekday()
		#print calendardate, calendardayofweek, calslinelist[dayofweek[calendardayofweek]]
		tripcountforday = int(calslinelist[dayofweek[calendardayofweek]])
		#print tripcountforday
		if tripcountforday > 0 :
			xinweek += tripcountforday
	trips_dict[in_id] = [slinelist[service_id_i], slinelist[route_id_i], xinweek]
	if xinweek > 0 : count_trip_ids_in_week +=1
	count += 1
	sline = filein.readline()
print '------------------'
#print trips_dict
print 'trips lines scanned ', count 
print 'trip ids in week ', count_trip_ids_in_week 
filein.close()

#
# scan routes.txt to create a routes dict keyed on route_id that includes a route_short_name, and agency_id
#
maxfilelinecount = MAX_ROUTES_COUNT
gtfsfile = 'routes.txt'
inid = 'route_id'
routes_dict = {}
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
#routes_dict = {keylist[inid_index]:[slinelist[agency_id_i], slinelist[route_short_name_i]]}
#print routes_dict
# scan gtfsfile
count = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	routes_dict[slinelist[inid_index]] = [slinelist[agency_id_i], slinelist[route_short_name_i]]
	count += 1
	sline = filein.readline()
print '------------------'
#print routes_dict
print 'last routes_dict entry entered: ', slinelist[inid_index], routes_dict[slinelist[inid_index]]
print '------------------'
print 'route lines scanned ', count 
filein.close()



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
# scan stops dict to populate trips per hour by looking up the each trip_id in the set in the trip dict
#   to get the service_id to look up the service days in the calendar dict
#   also update the total count 
#
print 'scan stops dict to populate trips per hour'
count = 0
tripcount = 0
maxtphanystop = 0
maxtpwanystop = 0
deltatimehist = []
for i in range(121) : deltatimehist.append(0)
for stop_id, [stop_lat, stop_lon, tripsatstop_dict, tphlist, totaltpwatstop] in stops_dict.iteritems():
	#print count, stop_id, stop_lat, stop_lon , len(tripsatstop_dict), tphlist, totaltpwatstop
	count += 1
	for trip_id, timeatstoplist in tripsatstop_dict.iteritems():
		tripcount +=1
		service_id = trips_dict[trip_id][0]
		slinelist = calendar_dict[service_id] # use service_id from trips_dict to look up calendar line list
		sstartcalendardate = slinelist[start_date_i] # string
		sendcalendardate = slinelist[end_date_i] # string
		startcalendardate = date(int(sstartcalendardate[0:4]),int(sstartcalendardate[4:6]),int(sstartcalendardate[6:8])) # start date for trip service
		endcalendardate = date(int(sendcalendardate[0:4]),int(sendcalendardate[4:6]),int(sendcalendardate[6:8])) # end date for trip service
		#print startcalendardate, endcalendardate, ' start and end date for trip service'
		#print startservicedate, endservicedate, ' start and end date for all service'
		route_id = trips_dict[trip_id][1]
		agency_id = routes_dict[route_id][0]
		route_short_name = routes_dict[route_id][1]
		#agency_name = agency_dict[agency_id]
		#line_name = agency_name+' - '+route_short_name # bigger file
		line_name = agency_id+'-'+route_short_name # smaller geojson file, but need to lookup agency name in client app for display
		#print count, tripcount, stop_id, trip_id, service_id, tpdlist[:2], totaltpwatstop
		#print 'route_id, line_name: ',route_id, line_name
		for ordcalendardate in range(max(startcalendardate.toordinal(),startservicedate.toordinal()),min(endcalendardate.toordinal(),endservicedate.toordinal())+1):
			calendardate = date.fromordinal(ordcalendardate)
			calendardayofweek = calendardate.weekday()
			#print calendardate, calendardayofweek, slinelist[dayofweek[calendardayofweek]]
			tripcountforday = int(slinelist[dayofweek[calendardayofweek]])
			#print tripcountforday
			if tripcountforday > 0 :
				maxtimetripatstop = 0
				mintimetripatstop = 30*60
				for timeatstop in timeatstoplist :
					hour_i = int(timeatstop[0:2])
					#print timeatstop, timeatstop[0:2], hour_i
					tphlist[hour_i] += tripcountforday # add to trip count for that day at the hour
					inttimeatstop = 60*int(timeatstop[0:2]) + int(timeatstop[3:5])
					maxtimetripatstop = max(maxtimetripatstop, inttimeatstop)
					mintimetripatstop = min(mintimetripatstop, inttimeatstop)
				deltatimetripatstop = maxtimetripatstop - mintimetripatstop
				if deltatimetripatstop < 120 : deltatimehist[deltatimetripatstop] +=1
				else : deltatimehist[120] +=1
				if deltatimetripatstop > 100 : print 'stop_id, trip_id, mintimetripatstop, maxtimetripatstop, deltatimetripatstop : ', stop_id, trip_id, mintimetripatstop, maxtimetripatstop, deltatimetripatstop
	#print count, stop_id, stops_dict[stop_id][3]
	totaltpwatstop = 0
	for tph in stops_dict[stop_id][3] :
		totaltpwatstop += tph
		maxtphanystop = max(maxtphanystop, tph)
	#print count, stop_id, totaltpwatstop
	stops_dict[stop_id][4] = totaltpwatstop
	maxtpwanystop = max(maxtpwanystop, totaltpwatstop)

print 'stop count ', count
#print 'last stops_dict entry : ', stops_dict[stop_id]
print 'maxtpwanystop ', maxtpwanystop
print 'maxtphanystop ', maxtphanystop
print deltatimehist
#
# >>> load txt file of stopsneartrainstop post edit
#
print '>>> load txt file of stopsneartrainstop post edit'
txtfilein = stopsneartrainstop_post_edit
stopsneartrainstop = {}
with open(processedpathin+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['trainstop_id', 'stop_id']
	print header
	for row in reader:
		#print row
		trainstop_id = row[0]
		stop_id = row[1]
		if trainstop_id == stop_id : # remove trainstop from list of stopsneartrainstop
			print trainstop_id
		else : # add to list
			if trainstop_id in stopsneartrainstop :
				stopsneartrainstop[trainstop_id].append(stop_id)
			else :
				stopsneartrainstop[trainstop_id] = [stop_id]
#print stopsneartrainstop[trainstop_id] # last one
print 'stopsneartrainstop loaded. trainstop count ', len(stopsneartrainstop)

#
# to create tripsneartrainstop_dict
# for each trainstop and stop near trainstop location 
#   merge the tripsatstop_dict from all stops near trainstop to create mergedtripsneartrainstop_dict
#
trainstopcount = 0
tripsneartrainstop_dict = {} # trainstop_id: mergedtripsneartrainstop_dict
# for each trainstop
# get near stop list to use as filter
for trainstop_id, stopsnearlist in stopsneartrainstop.iteritems():
	print trainstopcount, trainstop_id
	trainstopcount +=1
# for stops w tpd per line near trainstop
	mergedtripsneartrainstop_dict = {} # trip_id: [timeneartrainstop1, timeneartrainstop2, timeneartrainstop3...]
	stopneartrainstopcount = 0
	for stop_id in stopsnearlist :
		[stop_lat, stop_lon, tripsatstop_dict, tphlist, totaltpwatstop] = stops_dict[stop_id]
		stopneartrainstopcount +=1
#   merge the tripsatstop_dict from all stops near trainstop to create mergedtripsneartrainstop_dict
		for trip_id, timeatstoplist in tripsatstop_dict.iteritems() :
			if trips_dict[trip_id][2] > 0 : # xinweek > 0 then add first or merge otherwise don't add to dict at all
				if trip_id not in mergedtripsneartrainstop_dict: # not in merged dict then add it
					mergedtripsneartrainstop_dict[trip_id] = timeatstoplist
				else: # already in merged dict then append timeatstoplist
					mergedtripsneartrainstop_dict[trip_id].extend(timeatstoplist)
	tripsneartrainstop_dict[trainstop_id] = mergedtripsneartrainstop_dict
	print 'trainstop_id, len(mergedtripsneartrainstop_dict) : ', trainstop_id, len(mergedtripsneartrainstop_dict)
#print trainstop_id, mergedtripsneartrainstop_dict # last one
print 'trainstopcount, stopneartrainstopcount, ', trainstopcount, stopneartrainstopcount

#
# create tripswxinweekandminmaxtimesneartrainstop_dict by converting the list of times per trip near trainstop to 
# a list of min and max time for trip near trainstop and add also times per week that the trip is used
#

tripswxinweekandminmaxtimesneartrainstop_dict = {} # trainstop_id: tripswxinweekandminmaxtimes_dict
for trainstop_id, mergedtripsneartrainstop_dict in tripsneartrainstop_dict.iteritems() :
	tripswxinweekandminmaxtimes_dict ={} # trip_id: [xinweek, mintimetripatstop, maxtimetripatstop, deltatimetripatstop]
	for trip_id, timeatstoplist in mergedtripsneartrainstop_dict.iteritems() :
		maxtimetripatstop = 0
		mintimetripatstop = 30*60
		for timeatstop in timeatstoplist :
			inttimeatstop = 60*int(timeatstop[0:2]) + int(timeatstop[3:5])
			maxtimetripatstop = max(maxtimetripatstop, inttimeatstop)
			mintimetripatstop = min(mintimetripatstop, inttimeatstop)
		deltatimetripatstop = maxtimetripatstop - mintimetripatstop
		tripswxinweekandminmaxtimes_dict[trip_id] = [trips_dict[trip_id][2], mintimetripatstop, maxtimetripatstop, deltatimetripatstop] 
	tripswxinweekandminmaxtimesneartrainstop_dict[trainstop_id] = tripswxinweekandminmaxtimes_dict
	print 'trainstop_id, len(tripswxinweekandminmaxtimes_dict) : ', trainstop_id, len(tripswxinweekandminmaxtimes_dict)
#print trainstop_id, tripswxinweekandminmaxtimes_dict # last one

#
#   output to txt file
#
#
#   output txtfileout3 of trainstops with trips per hour in day summed over one week -'trainstops_w_tph_summed_over_week'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#
fileout = open(gtfspathout+txtfileout3, 'w') # save results in file
postsline = 'trainstop_id,tph00,tph01,tph02,tph03,tph04,tph05,tph06,tph07,tph08,tph09,tph10,tph11,tph12,tph13,tph14,tph15,tph16,tph17,tph18,tph19,tph20,tph21,tph22,tph23\n'
fileout.write(postsline)
for trainstop_id, tripswxinweekandminmaxtimes_dict in tripswxinweekandminmaxtimesneartrainstop_dict.iteritems() :
	tphlist24 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	tpwneartrainstop = 0
	count2x = 0
	count1x = 0
	for trip_id, [xinweek, mintimetripatstop, maxtimetripatstop, deltatimetripatstop] in tripswxinweekandminmaxtimes_dict.iteritems() :
		if deltatimetripatstop > 30 : 
			tpwneartrainstop += xinweek * 2
			count2x +=1
			hour_i = int(mintimetripatstop/60)%24
			tphlist24[hour_i] +=xinweek
			hour_i = int(maxtimetripatstop/60)%24
			tphlist24[hour_i] +=xinweek
			#print hour_i, maxtimetripatstop
		else :
			tpwneartrainstop += xinweek * 1
			count1x +=1
			hour_i = int(mintimetripatstop/60)%24
			tphlist24[hour_i] +=xinweek
	print trainstop_id, tphlist24, tpwneartrainstop, count2x, count1x
	stph24 = ''
	for i in range(24) : stph24 +=','+str(tphlist24[i])
	postsline = trainstop_id+stph24+'\n'
	fileout.write(postsline)
fileout.close()
print gtfspathout+txtfileout3

'''
#
#   output txtfileout1 of stops with trip_id s -'stops_w_trip_ids'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#
fileout = open(gtfspathout+txtfileout1, 'w') # save results in file
postsline = 'stop_id,trip_id\n'
fileout.write(postsline)
for stop_id, [stop_lat, stop_lon, tripsatstop_dict, tphlist, totaltpwatstop] in stops_dict.iteritems():
	for trip_id in tripsatstop_dict :
		if trips_dict[trip_id][2] > 0 : # if trip_id is used in service week analyzed then add to file
			postsline = stop_id+','+trip_id+'\n'
			fileout.write(postsline)
fileout.close()
print gtfspathout+txtfileout1

#
#   output txtfileout2 of stops with trips per hour in day summed over one week -'stops_w_tph_summed_over_week'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#
fileout = open(gtfspathout+txtfileout2, 'w') # save results in file
postsline = 'stop_id,tph00,tph01,tph02,tph03,tph04,tph05,tph06,tph07,tph08,tph09,tph10,tph11,tph12,tph13,tph14,tph15,tph16,tph17,tph18,tph19,tph20,tph21,tph22,tph23\n'
fileout.write(postsline)
for stop_id, [stop_lat, stop_lon, tripsatstop_dict, tphlist, totaltpwatstop] in stops_dict.iteritems():
	stphlist = ''
	for i in range(7) : stphlist += ','+str(tphlist[i]+tphlist[i+24])
	for i in range(7,24) : stphlist += ','+str(tphlist[i])
	postsline = stop_id+stphlist+'\n'
	fileout.write(postsline)
fileout.close()
print gtfspathout+txtfileout2
'''
'''
#
# scan stops_dict to create stopsforoutput_dict
# find day with max tpd and compute average tpd
# include in outputdict the tpdperline detail of the day with max tpd
# stopsforoutput_dict[stop_id] = [stop_lat, stop_lon, totaltripsatstop, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
#
count = 0
stopsforoutput_dict = {}
for stop_id, [stop_desc, stop_lat, stop_lon, tripsatstop_dict, tpdlist, totaltripsatstop] in stops_dict.iteritems():
	maxtpdatstop = 0
	maxdaytpdperline_dict = {}
	averagetpdatstop = totaltripsatstop/daysofservicetocount
	for [dayofservice, trips, tpdperline_dict] in tpdlist: # scan all service days per stop to find day with maxtpd and save tpdperline for that day
		if trips >= maxtpdatstop :
			maxtpdatstop = trips
			maxdaytpdperline_dict = tpdperline_dict
	stopsforoutput_dict[stop_id] = [stop_lat, stop_lon, totaltripsatstop, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
	#print count, stop_id
	count +=1
print 'stopsforoutput_dict created , len: ', len(stopsforoutput_dict), count
#print stop_id, stopsforoutput_dict[stop_id] # print last one

#
#   output js file of stops with max and average trips per day and tpd per line (agency_id, route short name) -'stops_w_tpd_per_line'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
#

def getJSON(s_id):
	return {
		"type": "Feature",
		"geometry": {
			"type": "Point",
			"coordinates": [float(stopsforoutput_dict[s_id][1]),float(stopsforoutput_dict[s_id][0])]
		},
		"properties": { 
			"stop_id": s_id,
			"totaltripsatstop": stopsforoutput_dict[s_id][2],
			"maxtpdatstop": stopsforoutput_dict[s_id][3],
			"averagetpdatstop": stopsforoutput_dict[s_id][4],
			"maxdaytpdperline_dict": stopsforoutput_dict[s_id][5]
		}
	}

# saveGeoJSON
print ("Generating GeoJSON export.")
geoj = {
	"type": "FeatureCollection",
	"features": [getJSON(stop_id) for stop_id in stopsforoutput_dict]
}
print ("Saving file: " + gtfspathout+jsfileout+ " ...")
nf = open(gtfspathout+jsfileout, "w")
jsonstr = json.dumps(geoj, separators=(',',':')) # smaller file for download
outstr = jsonstr.replace('}},', '}},\n')
nf.write('var stopsWtpdperline =\n')
nf.write(outstr)
nf.close()
print ("Saved file: " + jsfileout)

'''
