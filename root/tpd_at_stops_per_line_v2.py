#!/usr/bin/env python
# -*- coding: utf-8 -*-
# count the number of trips per day per line at all stops
# in a GTFS file over the selected week of the service period starting at serviceweekstartdate
# include breakdown of tpd per line (agency_id, route short name) at each stop
#
# inputs:
#   parent_path = 'C:\\transitanalyst\\gtfs\\'
#   pathout = 'C:\\transitanalyst\\processed\\'
#   sserviceweekstartdate = '20181021'
#   gtfsdate = '20181021'
#   gtfsdir = 'israel'+gtfsdate
#
# outputs:
#   output js file of stops with max and average trips per day and tpd per line (agency_id, route short name) -'stops_w_tpd_per_line'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
#   output geojson file of stops with max and average trips per day and tpd per line (agency_id, route short name) -'stops_w_tpd_per_line'+'_'+sserviceweekstartdate+'.geojson'
#
print('----------------- count the number of trips per day per line at all stops --------------------------')
print('output js file of stops with max and average trips per day and tpd per line (agency_id, route short name)')
from datetime import date
from datetime import timedelta
import time
import copy
import json
import gtfs_config as gtfscfg
from pathlib import Path

cwd = Path.cwd()
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
# scan lines in calendar to compute start and end service dates and to fill calendar_dict with calendar lines keyed on service_id
#
# create trips per day list with service day (from start to end) and count of 0 for tripsperday and empty tpdperline_dict
#   use as template for trips per day lists per stop
#
# scan stops.txt to create a stops dict keyed on stop_id that includes lat lon, an empty set of trip_id s for this stop and a 
# trips per day at stop list with service day (from start to end) and count of 0 for tripsperday and empty tpdperline_dict, and also stop desc
#   also calculate min and max lat lon
#
# scan stop_times.txt to populate trip_id set per stop in the stops dict
#
# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id
#
# scan routes.txt to create a routes dict keyed on route_id that includes a route_short_name, and agency_id
#
# scan agency.txt to create agency dict keyed on agency_id and includes agency name
#
# scan stops dict to populate trips per day by looking up the each trip_id in the set in the trip dict
#   to get the service_id to look up the service days in the calendar dict
#   also update the total count and add tpdperline to tpdperline_dict by looking up route_id in routes_dict to find route_short_name and agency_id
#
# output js file
#_________________________________
#
def main(gtfsdate, gtfsparentpath, gtfsdirbase, processedpath, serviceweekstartdate):
	# input:
	parent_path = cwd.parent / gtfsparentpath
	pathout = cwd.parent / processedpath
	sserviceweekstartdate = serviceweekstartdate # recommend to use gtfsdate (expect gtfs files to be most accurate for first week in service range)
	gtfsdir = gtfsdirbase+gtfsdate

	# output:
	jsfileout = 'stops_w_tpd_per_line'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'#   js file of stops with max and average tpd and tpd per line (agency_id, route short name) 
	geojsonfileout = 'stops_w_tpd_per_line'+'_'+sserviceweekstartdate+'.geojson' # geojson file of stops with max and average trips per day and tpd per line (agency_id, route short name)

	gtfspathin = parent_path / gtfsdir
	gtfspath = gtfspathin
	gtfspathout = pathout

	DAYSTOCOUNT = 7
	daysofservicetocount = DAYSTOCOUNT - DAYSTOCOUNT/7

	#
	# scan lines in calendar to compute start and end service dates and to fill calendar_dict with calendar lines keyed on service_id
	#
	maxfilelinecount = gtfscfg.MAX_CALENDAR_COUNT
	gtfsfile = 'calendar.txt'
	inid = 'service_id'
	calendar_dict = {}
	slinelist=[]
	print(gtfspath / gtfsfile)
	filein = open(gtfspath / gtfsfile, 'r', encoding="utf8")
	sline = filein.readline()
	slinelist=sline[:-1].split(",")
	print(slinelist)
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
	print('------------------')
	#print calendar_dict
	print(sstartservicedate, sendservicedate)
	filein.close()

	#
	# print int(sstartservicedate[0:4]),int(sstartservicedate[4:6]),int(sstartservicedate[6:8])
	# from str to date format
	startservicedate = date(int(sstartservicedate[0:4]),int(sstartservicedate[4:6]),int(sstartservicedate[6:8]))
	endservicedate = date(int(sendservicedate[0:4]),int(sendservicedate[4:6]),int(sendservicedate[6:8]))
	serviceweekstartdate = date(int(sserviceweekstartdate[0:4]),int(sserviceweekstartdate[4:6]),int(sserviceweekstartdate[6:8]))
	print('startservicedate, endservicedate, serviceweekstartdate ', startservicedate, endservicedate, serviceweekstartdate)

	#
	# create trips per day list with service day (from start to end) and count of 0, for tripsperday
	#   use as template for trips per day lists per stop
	#

	dateinservicerange = lambda d: d >= startservicedate and d <= endservicedate

	# print timedelta(days=1)
	serviceweekenddate = serviceweekstartdate + timedelta(days=DAYSTOCOUNT-1)
	print('serviceweekstartdate, serviceweekenddate ', serviceweekstartdate, serviceweekenddate)
	if dateinservicerange(serviceweekstartdate) and dateinservicerange(serviceweekenddate) :
		print('serviceweek selected is in service range') 
	else :
		print('error*********************serviceweek selected is NOT in service range: ' , serviceweekstartdate, serviceweekenddate, startservicedate, endservicedate)
		exit()

	print('startservicedate, endservicedate ', startservicedate, endservicedate)
	startservicedate = serviceweekstartdate
	endservicedate = serviceweekenddate
	print('startservicedate, endservicedate ', startservicedate, endservicedate)

	tripsperdaylist = []
	for ordservicedate in range (startservicedate.toordinal(), endservicedate.toordinal()+1):
		servicedate = date.fromordinal(ordservicedate)
		servicedayofweek = servicedate.weekday()
		print(servicedate, servicedayofweek)
		tripsperdaylist.append([servicedate, 0, {}])
	print('----tripsperdaylist----')
	for [dayofservice, tripsperday, tpdperline_dict] in tripsperdaylist:
		print(dayofservice, tripsperday, tpdperline_dict)

	#
	# scan stops.txt to create a stops dict keyed on stop_id that includes lat lon, an empty set of trip_id s for this stop and a 
	# trips per day at stop list with service day (from start to end) and count of 0 for tripsperday and empty tpdperline_dict, and also stop desc
	#   also calculate min and max lat lon#
	maxfilelinecount = gtfscfg.MAX_STOPS_COUNT
	gtfsfile = 'stops.txt'
	inid = 'stop_id'
	stops_dict = {}
	tripsperstop_set = set([]) # set of trip_id s of all trips that stop at this stop
	slinelist=[]
	print(gtfspath / gtfsfile)
	filein = open(gtfspath / gtfsfile, 'r', encoding="utf8")
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
	print('------------------')
	#print stops_dict
	#for stop_id, stopsdictlist in stops_dict.iteritems():
	#	print stop_id, stopsdictlist[:2], list(stopsdictlist[2])
	print('------------------')
	print('minlat, minlon : ', minlat, minlon)
	print('maxlat, maxlon : ', maxlat, maxlon)
	print('stop lines scanned ', count) 
	filein.close()

	#
	# scan stop_times.txt to populate trip_id set per stop in the stops dict
	#
	maxfilelinecount = gtfscfg.MAX_STOP_TIMES_COUNT
	gtfsfile = 'stop_times.txt'
	inid = 'stop_id'
	slinelist=[]
	print(gtfspath / gtfsfile)
	filein = open(gtfspath / gtfsfile, 'r', encoding="utf8")
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
		if slinelist[inid_index] in stops_dict:
			stops_dict[slinelist[inid_index]][trip_set_i].add(slinelist[trip_id_i])
			stopscount += 1
		count += 1
		sline = filein.readline()
	print('------------------')
	#print stops_dict
	#for stop_id in stops_dict: print stop_id, stops_dict[stop_id][:2], list(stops_dict[stop_id][2])[0:2]
	#print 'last stops_dict entry updated: ', stops_dict[slinelist[inid_index]]
	print('stop_times lines scanned ', count)
	print('stops found in dict ', stopscount) 
	print('maxlat, maxlon', maxlat, maxlon)
	filein.close()

	#
	# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id
	#
	maxfilelinecount = gtfscfg.MAX_TRIPS_COUNT
	gtfsfile = 'trips.txt'
	inid = 'trip_id'
	trips_dict = {}
	slinelist=[]
	print(gtfspath / gtfsfile)
	filein = open(gtfspath / gtfsfile, 'r', encoding="utf8")
	sline = filein.readline()
	slinelist=sline[:-1].split(",")
	# print slinelist
	keylist = slinelist
	inid_index = keylist.index(inid)
	trip_id_i = keylist.index('trip_id')
	service_id_i = keylist.index('service_id')
	route_id_i = keylist.index('route_id')
	trips_dict = {keylist[inid_index]:[slinelist[service_id_i], slinelist[route_id_i]]}
	print(trips_dict)
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
	print('------------------')
	#print trips_dict
	print('trips lines scanned ', count) 
	filein.close()

	#
	# scan routes.txt to create a routes dict keyed on route_id that includes a route_short_name, and agency_id
	#
	maxfilelinecount = gtfscfg.MAX_ROUTES_COUNT
	gtfsfile = 'routes.txt'
	inid = 'route_id'
	routes_dict = {}
	slinelist=[]
	print(gtfspath / gtfsfile)
	filein = open(gtfspath / gtfsfile, 'r', encoding="utf8")
	sline = filein.readline()
	slinelist=sline[:-1].split(",")
	print(slinelist)
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
	print('------------------')
	#print routes_dict
	print('last routes_dict entry entered: ', slinelist[inid_index], routes_dict[slinelist[inid_index]])
	print('------------------')
	print('route lines scanned ', count) 
	filein.close()

	'''
	#
	# scan agency.txt to create agency dict keyed on agency_id and includes agency name
	#
	maxfilelinecount = gtfscfg.MAX_AGENCY_COUNT
	gtfsfile = 'agency.txt'
	inid = 'agency_id'
	agency_dict = {}
	slinelist=[]
	print gtfspath / gtfsfile
	filein = open(gtfspath / gtfsfile, 'r', encoding="utf8")
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
	print agency_dict
	print 'agency lines scanned ', count 
	filein.close()
	'''

	#
	# scan stops dict to populate trips per day by looking up the each trip_id in the set in the trip dict
	#   to get the service_id to look up the service days in the calendar dict
	#   also update the total count and add tpdperline to tpdperline_dict by looking up route_id in routes_dict to find route_short_name and agency_id
	#

	count = 0
	tripcount = 0
	dayofweek=[monday_i, tuesday_i, wednesday_i, thursday_i, friday_i, saturday_i, sunday_i]
	maxtripsperdayanystop = 0
	maxtotaltripsanystop = 0
	for stop_id, [stop_desc, stop_lat, stop_lon, tripset, tpdlist, totaltpdatstop] in stops_dict.items():
		#print count, stop_id, stop_lat, stop_lon , len(tripset), list(tripset)[:2], tpdlist[:2], totaltpdatstop
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
			route_id = trips_dict[trip_id][1]
			agency_id = routes_dict[route_id][0]
			route_short_name = routes_dict[route_id][1]
			#agency_name = agency_dict[agency_id]
			#line_name = agency_name+' - '+route_short_name # bigger file
			line_name = agency_id+'-'+route_short_name # smaller geojson file, but need to lookup agency name in client app for display
			#print count, tripcount, stop_id, trip_id, service_id, tpdlist[:2], totaltpdatstop
			#print 'route_id, line_name: ',route_id, line_name
			for ordcalendardate in range(max(startcalendardate.toordinal(),startservicedate.toordinal()),min(endcalendardate.toordinal(),endservicedate.toordinal())+1):
				calendardate = date.fromordinal(ordcalendardate)
				calendardayofweek = calendardate.weekday()
				#print calendardate, calendardayofweek, slinelist[dayofweek[calendardayofweek]]
				if tpdlist[(calendardate-startservicedate).days][0] != calendardate :
					print('******error**************')
					print(tpdlist[(calendardate-startservicedate).days][0], calendardate) 
				tripcountforday = int(slinelist[dayofweek[calendardayofweek]])
				#print tripcountforday
				if tripcountforday > 0 :
					tpdlist[(calendardate-startservicedate).days][1] += tripcountforday # add to trip count for that day
					#print '(calendardate-startservicedate).days, tpdlist'
					#print (calendardate-startservicedate).days, tpdlist
					if (line_name in tpdlist[(calendardate-startservicedate).days][2]): # if line at stop on day counted already
						tpdlist[(calendardate-startservicedate).days][2][line_name] += tripcountforday # add count to tpdperline dict entry
					else :
						tpdlist[(calendardate-startservicedate).days][2][line_name] = tripcountforday # set count to tpdperline dict first time
		totaltripsatstop = 0
		maxtripsperdayatstop = 0
		for [dayofservice, trips, tpdperline_dict] in tpdlist: # scan all service days per stop to accumulate total trips at stop from trips per day at stop
			maxtripsperdayatstop = max(maxtripsperdayatstop, trips)
			totaltripsatstop += trips # and add to total trips at stop
		stops_dict[stop_id][5] = totaltripsatstop # changed from 4 when descs added
		maxtotaltripsanystop = max(maxtotaltripsanystop, totaltripsatstop)
		#print stop_id, tpdlist, totaltripsatstop
		if totaltripsatstop >= maxtotaltripsanystop : print(stop_id, stop_lat, stop_lon , list(tripset)[:2], tpdlist[:2], totaltripsatstop)
		#print 'maxtripsperdayatstop ', maxtripsperdayatstop
		#print 'maxtotaltripsanystop ', maxtotaltripsanystop
	print('count ', count)
	print('maxtotaltripsanystop ', maxtotaltripsanystop)

	'''
	#
	# output text file with total trip count per stop over service days counted - 'stopswtripcountand10xforrail.txt'
	#
	fileout = open(gtfspathout+stopswithtripcountfile, 'w', encoding="utf8") # save results in file
	postsline = 'stop_id,stop_lat,stop_lon,totaltripsatstop\n'
	fileout.write(postsline)
	for stop_id, [stop_desc, stop_lat, stop_lon, tripset, tpdlist, totaltripsatstop] in stops_dict.iteritems():
		if 'מסילת ברזל' in stop_desc :
			totaltripsatstop *=10
		postsline = stop_id+','+stop_lat+','+stop_lon+','+str(totaltripsatstop)+'\n'
		fileout.write(postsline)
	fileout.close()
	print gtfspathout+stopswithtripcountfile
	print 'stop_desc,stop_id,stop_lat,stop_lon,totaltripsatstop\n'
	print 'count ', count
	print 'maxtotaltripsanystop ', maxtotaltripsanystop

	'''

	#
	# scan stops_dict to create stopsforoutput_dict
	# find day with max tpd and compute average tpd
	# include in outputdict the tpdperline detail of the day with max tpd
	# stopsforoutput_dict[stop_id] = [stop_lat, stop_lon, totaltripsatstop, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
	#
	count = 0
	stopsforoutput_dict = {}
	for stop_id, [stop_desc, stop_lat, stop_lon, tripset, tpdlist, totaltripsatstop] in stops_dict.items():
		maxtpdatstop = 0
		maxdaytpdperline_dict = {}
		averagetpdatstop = round(totaltripsatstop/daysofservicetocount)
		for [dayofservice, trips, tpdperline_dict] in tpdlist: # scan all service days per stop to find day with maxtpd and save tpdperline for that day
			if trips >= maxtpdatstop :
				maxtpdatstop = trips
				maxdaytpdperline_dict = tpdperline_dict
		stopsforoutput_dict[stop_id] = [stop_lat, stop_lon, totaltripsatstop, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
		#print count, stop_id
		count +=1
	print('stopsforoutput_dict created , len: ', len(stopsforoutput_dict), count)
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

	# save GeoJSON and JS files
	print ("Generating GeoJSON export.")
	geoj = {
		"type": "FeatureCollection",
		"features": [getJSON(stop_id) for stop_id in stopsforoutput_dict]
	}
	print(("Saving file: ", gtfspathout / jsfileout, " ..."))
	nf = open(gtfspathout / jsfileout, "w", encoding="utf8")
	jsonstr = json.dumps(geoj, separators=(',',':')) # smaller file for download
	outstr = jsonstr.replace('}},', '}},\n')
	nf.write('var stopsWtpdperline =\n')
	nf.write(outstr)
	nf.close()
	print(("Saved file: " + jsfileout))
	
	print(("Saving file: ", gtfspathout / geojsonfileout, " ..."))
	nf = open(gtfspathout / geojsonfileout, "w", encoding="utf8")
	nf.write(outstr)
	nf.close()
	print(("Saved file: " + geojsonfileout))



