#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create a file with average trips per day (tpd) at all stops
# count the number of trips per day at all stops in a GTFS file over one week of the entire service period starting at serviceweekstartdate
#
# input:
#   gtfspathin = 'C:\\transitanalyst\\gtfs\\'
#   pathout = 'C:\\transitanalyst\\processed\\'
#   sserviceweekstartdate = '20180425'
#   gtfsdate = '20180425'
#   gtfsdir = 'israel'+gtfsdate
#
# output:
#   txt file with average tpd per stop  - 'stopswtpdand10xforrail'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#
#
print '----------------- create a file with average trips per day (tpd) at all stops --------------------------'
print 'generate stopswtpdand10xforrail_[serviceweekstartdate]_[gtfsdate].txt'
from datetime import date
from datetime import timedelta
import time
import copy

print "Local current time :", time.asctime( time.localtime(time.time()) )
#
# scan lines in calendar to compute start and end service dates and to fill calendar_dict with calendar lines keyed on service_id
#
# create trips per day list with service day (from start to end) and count of 0 for tripsperday
#   use as template for trips per day lists per stop
#
# scan stops.txt to create a stops dict keyed on stop_id that includes lat lon, an empty set of trip_id s for this stop and a 
# trips per day at stop list with service day (from start to end) and count of 0, and also stop desc
#   also calculate min and max lat lon
#
# scan stop_times.txt to populate trip_id set per stop in the stops dict
#
# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id
#
# scan stops dict to populate trips per day by looking up the each trip_id in the set in the trip dict
#   to get the service_id to look up the service days in the calendar dict
#   also update the total count and multiply 10x for rail
#_________________________________
#
# input:
gtfspathin = 'C:\\transitanalyst\\gtfs\\'
pathout = 'C:\\transitanalyst\\processed\\'
sserviceweekstartdate = '20180425' # recommend to use gtfsdate (expect gtfs files to be most accurate for first week in service range)
gtfsdate = '20180425'
gtfsdir = 'israel'+gtfsdate

# output:
txtfileout = 'stopswtpdand10xforrail'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'#   txt file with average tpd per stop 

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
gtfspath = gtfspathin+gtfsdir+'\\'
gtfsfile = 'calendar.txt'
inid = 'service_id'
calendar_dict = {}
tripsperdaylist = []
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
# create trips per day list with service day (from start to end) and count of 0, for tripsperday
#   use as template for trips per day lists per stop
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

for ordservicedate in range (startservicedate.toordinal(), endservicedate.toordinal()+1):
	servicedate = date.fromordinal(ordservicedate)
	servicedayofweek = servicedate.weekday()
	print servicedate, servicedayofweek
	tripsperdaylist.append([servicedate, 0])
print '----tripsperdaylist----'
for [dayofservice, tripsperday] in tripsperdaylist:
	print dayofservice, tripsperday

#
# scan stops.txt to create a stops dict keyed on stop_id that includes lat lon, an empty set of trip_id s for this stop and a 
# trips per day at stop list with service day (from start to end) and count of 0, and also stop desc
#   also calculate min and max lat lon
#
maxfilelinecount = MAX_STOPS_COUNT
gtfsfile = 'stops.txt'
inid = 'stop_id'
stops_dict = {}
tripsperstop_set = set([]) # set of trip_id s of all trips that stop at this stop
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
#stops_dict = {keylist[inid_index]:[slinelist[stop_desc_i], slinelist[stop_lat_i], slinelist[stop_lon_i], set(['trip_id']),copy.deepcopy(tripsperdaylist), 0]}
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
	stops_dict[slinelist[inid_index]] = [slinelist[stop_desc_i], slinelist[stop_lat_i], slinelist[stop_lon_i], set([]), copy.deepcopy(tripsperdaylist), 0]
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
print 'stop lines scanned ', count 
print '-------------------------------------------'
print 'stops minlat, minlon : ', minlat, minlon
print 'stops maxlat, maxlon : ', maxlat, maxlon

filein.close()

'''
ilminlat = 29.490000 # Israel min lat
ilminlon = 34.280000 # Israel min lon
ilmaxlat = 33.290000 # Israel max lat
ilmaxlon = 35.840000 # Israel max lon

gridorglat = ilminlat # grid origin lat
gridorglon = ilminlon # grid origin lon

lat100 = 0.0011100 # grid step of 100m
lon100 = 0.0009600 # grid step of 100m

grid_id = lambda lat, lon: (int((float(lat)-gridorglat)//lat100), int((float(lon)-gridorglon)//lon100));
print 'minlatlon grid_id ', grid_id(minlat, minlon)
print 'maxlatlon grid_id ', grid_id(maxlat, maxlon)
'''

#
# scan stop_times.txt to populate trip_id set per stop in the stops dict
#
maxfilelinecount = MAX_STOP_TIMES_COUNT
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
trip_set_i = 3; # changed from 2 when stop_desc added
#stops_dict[keylist[stop_id_i]][trip_set_i].add(keylist[trip_id_i])
# scan gtfsfile
count = 0
stopscount = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	if stops_dict.has_key(slinelist[inid_index]):
		stops_dict[slinelist[inid_index]][trip_set_i].add(slinelist[trip_id_i])
		stopscount += 1
	count += 1
	sline = filein.readline()
print '------------------'
#print stops_dict
#for stop_id in stops_dict: print stop_id, stops_dict[stop_id][:2], list(stops_dict[stop_id][2])[0:2]
print 'stop_times lines scanned ', count
print 'stops found in dict ', stopscount 
print 'maxlat, maxlon', maxlat, maxlon
filein.close()

#
# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id
#
maxfilelinecount = MAX_TRIPS_COUNT

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
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	slinelist=sline[:-1].split(",")
	#print slinelist
	in_id = slinelist[inid_index]
	# print in_id
	trips_dict[in_id] = [slinelist[service_id_i], slinelist[route_id_i]]
	count += 1
	sline = filein.readline()
print '------------------'
#print trips_dict
print 'trips lines scanned ', count 
filein.close()

#
# scan stops dict to populate trips per day by looking up the each trip_id in the set in the trip dict
#   to get the service_id to look up the service days in the calendar dict
#   also update the total count
#

count = 0
tripcount = 0
dayofweek=[monday_i, tuesday_i, wednesday_i, thursday_i, friday_i, saturday_i, sunday_i]
maxtripsperdayanystop = 0
maxtotaltripsanystop = 0
for stop_id, [stop_desc, stop_lat, stop_lon, tripset, tpdlist, totaltpdatstop] in stops_dict.iteritems():
	#print stop_id, stop_lat, stop_lon , list(tripset)[:2], tpdlist[:2], totaltripsatstop
	count += 1
	for trip_id in tripset:
		tripcount +=1
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
	totaltripsatstop = 0
	maxtripsperdayatstop = 0
	for [dayofservice, trips] in tpdlist: # scan all service days per stop to accumulate total trips at stop from trips per day at stop
		maxtripsperdayatstop = max(maxtripsperdayatstop, trips)
		totaltripsatstop += trips # and add to total trips at stop
	stops_dict[stop_id][5] = totaltripsatstop # changed from 4 when descs added
	maxtotaltripsanystop = max(maxtotaltripsanystop, totaltripsatstop)
	#print stop_id, stop_lat, stop_lon , list(tripset)[:2], tpdlist, totaltripsatstop
	if totaltripsatstop>9000 : print stop_id, stop_lat, stop_lon , list(tripset)[:2], tpdlist, totaltripsatstop
	#print 'maxtripsperdayatstop ', maxtripsperdayatstop
	#print 'maxtotaltripsanystop ', maxtotaltripsanystop
print 'count ', count
print 'maxtotaltripsanystop before 10x for rail', maxtotaltripsanystop

fileout = open(pathout+txtfileout, 'w') # save results in file
postsline = 'stop_id,stop_lat,stop_lon,averagetpdatstop\n'
fileout.write(postsline)
for stop_id, [stop_desc, stop_lat, stop_lon, tripset, tpdlist, totaltpdatstop] in stops_dict.iteritems():
	#print grid_key, rawtransitscore
	if 'מסילת ברזל' in stop_desc :
		totaltpdatstop *=10
	postsline = stop_id+','+stop_lat+','+stop_lon+','+str(totaltpdatstop/daysofservicetocount)+'\n' # calculate average tpd by using 6 service days per week
	fileout.write(postsline)
	maxtotaltripsanystop = max(maxtotaltripsanystop, totaltpdatstop)
fileout.close()
print pathout+txtfileout
print 'stop_desc,stop_id,stop_lat,stop_lon,averagetpdatstop\n'
print 'count ', count
print 'maxtotaltripsanystop, maxaveragetpdatanystop after 10x for rail', maxtotaltripsanystop, maxtotaltripsanystop/daysofservicetocount

