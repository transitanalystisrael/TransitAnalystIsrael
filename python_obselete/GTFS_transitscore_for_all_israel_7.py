#!/usr/bin/env python
#--------------------------------------------------
# Create transitscore files from GTFS for all of Israel
# input GTFS dir israelyyyymmdd is expected in transitanalyst\\gtfs directory  
#------------------------------------------------------------------------------------------
import os
import sys
from datetime import date
from datetime import timedelta
import time
import copy
import math
import gtfs_config as gtfscfg

print '# input GTFS dir israelyyyymmdd is expected in transitanalyst\\gtfs directory  '

def main(gtfsdate, gtfspath, gtfsdirbase, processedpath):

	gtfsdir = gtfsdirbase+gtfsdate
	gtfspathin = gtfspath
	gtfsdirin = gtfspathin+gtfsdir+'\\'
	gtfspathout = processedpath

	gridfileraw = 'raw_transit_score_'+gtfsdir+'.txt'
	gridfile = 'transit_score_'+gtfsdir+'.txt'
	pointfile = 'transit_score_point_'+gtfsdir+'.csv'
	
	DAYSTOCOUNT = 7

	#------------------------------------------------------------------------
	# count the number of trips per day in a 100x100m area around a given lat-lon
	# in a GTFS file over the first week of the entire service period
	#
	print '----------------- trips per day for lat-lon grid --------------------------'
	print "Local current time :", time.asctime( time.localtime(time.time()) )
	#
	# scan stops.txt to create a stops dict keyed on stop_id that includes lat lon and an empty set of trip_id s for this stop,
	#   also calculate min and max lat lon
	#
	# scan stop_times.txt to populate trip_id set per stop in the stops dict
	#
	# scan lines in calendar to compute start and end service dates and to fill calendar_dict with calendar lines keyed on service_id
	#
	# create trips per day list with service day (from start to end) and count of 0,
	#   use as tempale for trips per day lists per grid element
	#
	# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id
	#
	# scan stops dict to create grid dict keyed on grid_id that includes a set of trip_id s and
	#   3 lists for trips per day (s, m, l) for each grid element
	#
	# scan grid dict to populate trips per day by looking up the each trip in the set in the trip dict
	#   to get the service_id to look up the service days in the calendar dict 
	# 
	#_________________________________
	#

	# scan stops.txt to create a stops dict keyed on stop_id that includes lat lon and an empty set of trip_id s for this stop,
	#   also calculate min and max lat lon
	#
	maxfilelinecount = gtfscfg.MAX_STOPS_COUNT
	gtfspath = gtfsdirin
	gtfsfile = 'stops.txt'
	inid = 'stop_id'
	stops_dict = {}
	tripsperstop_set = set([]) # set of trip_id s of all trips that stop at this stop
	slinelist=[]
	print gtfspath+gtfsfile
	filein = open(gtfspath+gtfsfile, 'r')
	sline = filein.readline()
	slinelist=sline[:-1].split(",")
	print slinelist
	keylist = slinelist
	inid_index = keylist.index(inid)
	stop_id_i = keylist.index('stop_id')
	stop_lat_i = keylist.index('stop_lat')
	stop_lon_i = keylist.index('stop_lon')
	#stops_dict = {keylist[inid_index]:[slinelist[stop_lat_i], slinelist[stop_lon_i], set(['trip_id'])]}
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
		stops_dict[slinelist[inid_index]] = [slinelist[stop_lat_i], slinelist[stop_lon_i], set([])]
		minlat = min(minlat, slinelist[stop_lat_i])
		maxlat = max(maxlat, slinelist[stop_lat_i])
		minlon = min(minlon, slinelist[stop_lon_i])
		maxlon = max(maxlon, slinelist[stop_lon_i])
		count += 1
		sline = filein.readline()
	print '------------------'
	#print stops_dict
	#for stop_id, stopsdictlist in stops_dict.iteritems():
	#    print stop_id, stopsdictlist[:2], list(stopsdictlist[2])
	print '------------------'
	print minlat, minlon
	print maxlat, maxlon
	print 'stop lines scanned ', count 
	filein.close()

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

	grid_point = lambda grid_id_lat, grid_id_lon: [gridorglon+lon100*float(grid_id_lon)+lon100/2, gridorglat+lat100*float(grid_id_lat)+lat100/2]

	#
	# scan stop_times.txt to populate trip_id set per stop in the stops dict
	#
	maxfilelinecount = gtfscfg.MAX_STOP_TIMES_COUNT
	gtfspath = gtfsdirin
	gtfsfile = 'stop_times.txt'
	inid = 'stop_id'
	slinelist=[]
	print gtfspath+gtfsfile
	filein = open(gtfspath+gtfsfile, 'r')
	sline = filein.readline()
	slinelist=sline[:-1].split(",")
	print slinelist
	keylist = slinelist
	inid_index = keylist.index(inid)
	stop_id_i = keylist.index('stop_id')
	trip_id_i = keylist.index('trip_id')
	trip_set_i = 2;
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
	# scan lines in calendar to compute start and end service dates and to fill calendar_dict with calendar lines keyed on service_id
	#
	maxfilelinecount = gtfscfg.MAX_CALENDAR_COUNT
	gtfsfile = 'calendar.txt'
	inid = 'service_id'
	calendar_dict = {}
	tripsperdaylist = []
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
	# create trips per day list with service day (from start to end) and count of 0, 0, 0, 0 for trips_s, trips_m, trips_l, trips_total
	#   use as template for trips per day lists per grid element
	#
	# print timedelta(days=1)
	if (endservicedate.toordinal()-startservicedate.toordinal()) > 	DAYSTOCOUNT : endservicedate = startservicedate + timedelta(days=DAYSTOCOUNT-1)
	print 'startservicedate, endservicedate ', startservicedate, endservicedate
	for ordservicedate in range (startservicedate.toordinal(), endservicedate.toordinal()+1):
		servicedate = date.fromordinal(ordservicedate)
		servicedayofweek = servicedate.weekday()
		print servicedate, servicedayofweek
		tripsperdaylist.append([servicedate, 0, 0, 0, 0])
	#print tripsperdaylist
	for [dayofservice, trips_s, trips_m, trips_l, trips_total] in tripsperdaylist:
		print dayofservice, trips_s, trips_m, trips_l, trips_total

	#
	# scan trips.txt to create trips dict keyed on trip_id and includes service_id and route_id
	#
	maxfilelinecount = gtfscfg.MAX_TRIPS_COUNT
	gtfspath = gtfsdirin
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
	# scan stops dict to create grid dict keyed on grid_id that includes a set of stop_id s, a set of trip_id s,
	#   4 lists for trips per day (s, m, l and total) for each grid element and a raw transit score of 0 per grid element
	#
	m_size = 5 # 500m square around grid element (note - set to odd number)
	l_size = 9 # 900m square around grid element (note - set to odd number bigger than m)
	band_m_s = (m_size-1)/2
	band_l_s = (l_size-1)/2
	band_l_m = (l_size-m_size)/2
	grid_dict = {}
	count = 0
	newcount = 0
	for stop_id, [stop_lat, stop_lon, tripset] in stops_dict.iteritems():
		#print stop_id, stop_lat, stop_lon , list(tripset)[:2]
		count += 1
		grid_key = grid_id(stop_lat, stop_lon)
		if grid_dict.has_key(grid_key):
			# update grid item
			grid_dict[grid_key][0] |= set([stop_id])
			grid_dict[grid_key][1]|= tripset
		else:
			# create new grid item
			newcount +=1
			grid_dict[grid_key] = [set([stop_id]), tripset, copy.deepcopy(tripsperdaylist), 0]
	#for grid_key, [stopset, tripset, tpdlist] in grid_dict.iteritems(): print grid_key, list(stopset)[:1], list(tripset)[:1], tpdlist[:][1][0:2]
	print 'count, newcount ', count, newcount

	#
	# scan grid dict to create grid elements around grid elements with stops in them
	#
	gridcount = 0
	newcount = 0
	gridaroundstopsset = set([])
	totalgridelements = len(grid_dict)
	print 'totalgridelements before add around stops ', totalgridelements
	for grid_key, [stopset, tripset, tpdlist, rawtransitscore] in grid_dict.iteritems():
		gridcount +=1
		#print grid_key, gridcount, totalgridelements
		for lat_i in range(grid_key[0]-band_l_s, grid_key[0]+band_l_s+1):
			if lat_i < 0 : break
			for lon_i in range(grid_key[1]-band_l_s, grid_key[1]+band_l_s+1):
				if lon_i < 0 : break
				#print lat_i, lon_i
				if not grid_dict.has_key((lat_i, lon_i)):
					# collect new grid item
					newcount +=1
					gridaroundstopsset.add((lat_i, lon_i))

	print 'gridcount, newcount, len(gridaroundstopsset) ', gridcount, newcount, len(gridaroundstopsset)
	# now that we collected grid elements to add then add them
	count = 0
	for (lat_i, lon_i) in gridaroundstopsset:
		#print count, newcount
		count +=1
		grid_dict[(lat_i, lon_i)] = [set([]), set([]), copy.deepcopy(tripsperdaylist), 0]

	totalgridelements = len(grid_dict)
	print 'totalgridelements after add around stops ', totalgridelements

	#
	# scan grid dict to populate trips per day by looking up each trip in the set in the trip dict
	#   to get the service_id to look up the service days in the calendar dict 
	#
	print 'scan grid dict to populate trips per day by looking up each trip in the set in the trip dict to get the service_id to look up the service days in the calendar dict'
	dayofweek=[monday_i, tuesday_i, wednesday_i, thursday_i, friday_i, saturday_i, sunday_i]
	gridcount = 0
	tripcount = 0
	maxtripsperday_s = 0
	maxtripsperday_m = 0
	maxtripsperday_l = 0
	maxtripsperday_total = 0
	maxrawtransitscore = 0.0
	weight_s = 1.0
	weight_m = 0.8
	weight_l = 0.5
	totalgridelements = len(grid_dict)
	for grid_key, [stopset, tripset, tpdlist, rawtransitscore] in grid_dict.iteritems():
		gridcount +=1
		#print grid_key, gridcount, totalgridelements
		for trip_id in tripset:
			tripcount +=1
			service_id = trips_dict[trip_id][0]
			slinelist = calendar_dict[service_id] # use service_id from line in trips.txt to look up calendar line list
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
				maxtripsperday_s = max(maxtripsperday_s, tpdlist[(calendardate-startservicedate).days][1])
				tpdlist[(calendardate-startservicedate).days][4] += int(slinelist[dayofweek[calendardayofweek]]) # and add to total trips
				maxtripsperday_total = max(maxtripsperday_total, tpdlist[(calendardate-startservicedate).days][4])
				rawtransitscore += weight_s*int(slinelist[dayofweek[calendardayofweek]]) # and add to raw transit score after applying weight
		# collect the trips around the grid_key
		tripset_m_s = set([])
		grid_key_list_m =[]
		for lat_i in range(grid_key[0]-band_m_s, grid_key[0]+band_m_s+1):
			if lat_i < 0 : break
			for lon_i in range(grid_key[1]-band_m_s, grid_key[1]+band_m_s+1):
				if lon_i < 0 : break
				#print lat_i, lon_i
				grid_key_list_m.append((lat_i, lon_i))
				if grid_dict.has_key((lat_i, lon_i)):
					tripset_m_s |= grid_dict[(lat_i, lon_i)][1]
		tripset_m_s -= tripset # remove trips in grid_key itself to get only additional trips
		# lookup and count per day the trips around the grid_key
		for trip_id in tripset_m_s:
			tripcount +=1
			service_id = trips_dict[trip_id][0]
			slinelist = calendar_dict[service_id] # use service_id from line in trips.txt to look up calendar line list
			sstartcalendardate = slinelist[start_date_i]
			sendcalendardate = slinelist[end_date_i]
			startcalendardate = date(int(sstartcalendardate[0:4]),int(sstartcalendardate[4:6]),int(sstartcalendardate[6:8])) # start date for trip service
			endcalendardate = date(int(sendcalendardate[0:4]),int(sendcalendardate[4:6]),int(sendcalendardate[6:8])) # end date for trip service
			# print startcalendardate, endcalendardate, ' start and end date for trip service'
			for ordcalendardate in range(max(startcalendardate.toordinal(),startservicedate.toordinal()),min(endcalendardate.toordinal(),endservicedate.toordinal())+1):
				calendardate = date.fromordinal(ordcalendardate)
				calendardayofweek = calendardate.weekday()
				#print calendardate, calendardayofweek, slinelist[dayofweek[calendardayofweek]]
				if tpdlist[(calendardate-startservicedate).days][0] != calendardate :
					print '******error**************'
					print tpdlist[(calendardate-startservicedate).days][0], calendardate 
				tpdlist[(calendardate-startservicedate).days][2] += int(slinelist[dayofweek[calendardayofweek]]) # add to trip count for that day
				tpdlist[(calendardate-startservicedate).days][4] += int(slinelist[dayofweek[calendardayofweek]]) # and add to total trips
		# collect the trips around the grid_key at the second level
		tripset_l_m = set([])
		grid_key_list_l =[]
		for lat_i in range(grid_key[0]-band_l_s, grid_key[0]+band_l_s+1):
			if lat_i < 0 : break
			for lon_i in range(grid_key[1]-band_l_s, grid_key[1]+band_l_s+1):
				if lon_i < 0 : break
				#print lat_i, lon_i
				grid_key_list_l.append((lat_i, lon_i))
				if grid_dict.has_key((lat_i, lon_i)):
					tripset_l_m |= grid_dict[(lat_i, lon_i)][1]
		tripset_l_m -= tripset_m_s # remove trips around grid_key itself to get only additional trips
		tripset_l_m -= tripset # remove trips in grid_key itself to get only additional trips
		# lookup and count per day the trips around the grid_key
		for trip_id in tripset_l_m:
			tripcount +=1
			service_id = trips_dict[trip_id][0]
			slinelist = calendar_dict[service_id] # use service_id from line in trips.txt to look up calendar line list
			sstartcalendardate = slinelist[start_date_i]
			sendcalendardate = slinelist[end_date_i]
			startcalendardate = date(int(sstartcalendardate[0:4]),int(sstartcalendardate[4:6]),int(sstartcalendardate[6:8])) # start date for trip service
			endcalendardate = date(int(sendcalendardate[0:4]),int(sendcalendardate[4:6]),int(sendcalendardate[6:8])) # end date for trip service
			# print startcalendardate, endcalendardate, ' start and end date for trip service'
			for ordcalendardate in range(max(startcalendardate.toordinal(),startservicedate.toordinal()),min(endcalendardate.toordinal(),endservicedate.toordinal())+1):
				calendardate = date.fromordinal(ordcalendardate)
				calendardayofweek = calendardate.weekday()
				#print calendardate, calendardayofweek, slinelist[dayofweek[calendardayofweek]]
				if tpdlist[(calendardate-startservicedate).days][0] != calendardate :
					print '******error**************'
					print tpdlist[(calendardate-startservicedate).days][0], calendardate 
				tpdlist[(calendardate-startservicedate).days][3] += int(slinelist[dayofweek[calendardayofweek]]) # add to trip count for that day
				tpdlist[(calendardate-startservicedate).days][4] += int(slinelist[dayofweek[calendardayofweek]]) # and add to total trips
				
		rawtransitscore = 0.0
		for [dayofservice, trips_s, trips_m, trips_l, trips_total] in tpdlist:
			maxtripsperday_s = max(maxtripsperday_s, trips_s)
			maxtripsperday_m = max(maxtripsperday_m, trips_m)
			maxtripsperday_l = max(maxtripsperday_l, trips_l)
			maxtripsperday_total = max(maxtripsperday_total, trips_total)
			rawtransitscore += (weight_s*trips_s+weight_m*trips_m+weight_l*trips_l) # and add to raw transit score after applying weight
		grid_dict[grid_key][3] = rawtransitscore
		maxrawtransitscore = max(maxrawtransitscore, rawtransitscore)    

	#
	# output grid id based rawtransitscore file 
	#
	#gridfile = 'grid_scores.txt'
	print 'output to gridfileraw ', gtfspathout+gridfileraw
	fileout = open(gtfspathout+gridfileraw, 'w')
	postsline = 'grid_lat_i,grid_lon_i,rawtransitscore\n'
	fileout.write(postsline)
	for grid_key, [stopset, tripset, tpdlist, rawtransitscore] in grid_dict.iteritems():
		#print grid_key, rawtransitscore
		postsline = str(grid_key[0])+','+str(grid_key[1])+','+str(rawtransitscore)+'\n'
		fileout.write(postsline)
	fileout.close()

	#for grid_key, [stopset, tripset, tpdlist] in grid_dict.iteritems(): print grid_key, list(stopset)[:1], list(tripset)[:1], tpdlist[:][1][0:2]
	print 'gridcount, tripcount ', gridcount, tripcount
	print 'max: tpd_s, tpd_m, tpd_l, tpd_total, rawscore', maxtripsperday_s, maxtripsperday_m, maxtripsperday_l, maxtripsperday_total, maxrawtransitscore

	#
	# output csv file of lat lon points with transitscore
	#
	print 'output to pointfile ', gtfspathout+pointfile
	fileout = open(gtfspathout+pointfile, 'w')
	postsline = 'grid_lat,grid_lon,transitscore\n'
	fileout.write(postsline)
	for grid_key, [stopset, tripset, tpdlist, rawtransitscore] in grid_dict.iteritems():
		#print grid_key, rawtransitscore
		if rawtransitscore > 1 :
			transitscore = round(100.0*math.log10(rawtransitscore)/math.log10(maxrawtransitscore))
		else:
			transitscore = 0
		point = grid_point(grid_key[0],grid_key[1])
		postsline = str(point[1])+','+str(point[0])+','+str(int(transitscore))+'\n'
		fileout.write(postsline)
	fileout.close()

	#
	# output grid id based transitscore file 
	#
	#gridfile = 'grid_scores.txt'
	print 'output to gridfile ', gtfspathout+gridfile
	fileout = open(gtfspathout+gridfile, 'w')
	postsline = 'grid_lat_i,grid_lon_i,transitscore\n'
	fileout.write(postsline)
	for grid_key, [stopset, tripset, tpdlist, rawtransitscore] in grid_dict.iteritems():
		#print grid_key, rawtransitscore
		if rawtransitscore > 1 :
			transitscore = round(100.0*math.log10(rawtransitscore)/math.log10(maxrawtransitscore))
		else:
			transitscore = 0
		postsline = str(grid_key[0])+','+str(grid_key[1])+','+str(int(transitscore))+'\n'
		fileout.write(postsline)
	fileout.close()

