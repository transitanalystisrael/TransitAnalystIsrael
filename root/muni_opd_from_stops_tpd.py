#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create a file with transit opportunities per day (opd) at munis 
# filter file with average tpd per stop and stop location, using muni boarder multipolygons in geojson files
# sum tpds at stops in muni to calculate opd for muni
#
# input:
#   gtfsdate = '20180425'
#   sserviceweekstartdate = '20180425'
#   pathin = 'C:\\transitanalyst\\processed\\'
#   pathout = 'C:\\transitanalyst\\processed\\'
#   txt file with average tpd per stop  - 'stopswtpdand10xforrail'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#   israel_city_boarders.geojson
#   israel_town_boarders.geojson # moatzot mekomiyot
#
# output:
#   txt file with average opd per muni  - 'muni_opd'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#
#
print('----------------- create a file with transit opportunities per day (opd) at munis --------------------------')
print('sum tpds at stops in muni to calculate opd for muni')
print('generate muni_opd_[serviceweekstartdate]_[gtfsdate].txt')
from datetime import date
from datetime import timedelta
import time
import copy
import os
import json
from shapely.geometry import shape, Point, Polygon, MultiPolygon
import gtfs_config as gtfscfg
from pathlib import Path

cwd = Path.cwd()

def main(gtfsdate, processedpath, serviceweekstartdate):
	# input:
	sserviceweekstartdate = serviceweekstartdate
	pathin = cwd.parent / processedpath
	pathout = cwd.parent / processedpath
	stopsfilein = 'stopswtpdand10xforrail'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt' # txt file with average tpd per stop and top location
	cityfilein = 'israel_city_boarders.geojson'
	townfilein = 'israel_town_boarders.geojson' # moatzot mekomiyot

	# output:
	munifileout = stopsfilein.replace('stopswtpdand10xforrail', 'muni_opd') #  txt file with average opd per muni 
	print('stopsfilein, munifileout : ', stopsfilein, munifileout)


	'''

	muniboarderfile = 'israel_muni_boarders_filtered_v3.txt'
	muniboarderandtripcountfile = 'israel_muni_boarders_and_trip_count.txt'
	munitransitfile = 'israel_muni_transit.txt'
	munistopsfile = 'stopswtripcountand10xforrail.txt'
	munikmlfile = 'israel_muni_boarders.kml'

	kml = Kml()
	'''
	gtfspathin = pathin
	gtfspathout = pathout

	#
	# load files 
	#

	#
	# scan stopfile to create munistops_dict and compute maxaveragetpdatstop and totaltripsatallstops
	#
	# 1st sline is 'stop_id,stop_lat,stop_lon,averagetpdatstop\n'
	#
	maxaveragetpdatstop = 0.0
	totaltripsatallstops = 0.0

	munistops_dict = {}
	slinelist=[]
	print(gtfspathin / stopsfilein)
	filein = open(gtfspathin / stopsfilein, 'r', encoding="utf8")
	sline = filein.readline()
	keylinelen = len(sline)
	slinelist=sline[:-1].split(",")
	print(slinelist)
	keylist = slinelist
	stop_id_i = keylist.index('stop_id')
	stop_lat_i = keylist.index('stop_lat')
	stop_lon_i = keylist.index('stop_lon')
	averagetpdatstop_i = keylist.index('averagetpdatstop')
	print(slinelist[stop_id_i], slinelist[stop_lat_i], slinelist[stop_lon_i], slinelist[averagetpdatstop_i])
	maxfilelinecount = gtfscfg.MAX_STOPS_COUNT
	count = 0
	sline = filein.readline()
	fileinlines = (os.path.getsize(gtfspathin / stopsfilein)-keylinelen)/len(sline)
	# scan stopsfilein
	while ((count < maxfilelinecount) and (sline != '')):
		slinelist=sline[:-1].split(",")
		#print (slinelist)
		stop_id = slinelist[stop_id_i]
		stop_lat = slinelist[stop_lat_i]
		stop_lon = slinelist[stop_lon_i]
		averagetpdatstop = float(slinelist[averagetpdatstop_i])
		maxaveragetpdatstop = max(maxaveragetpdatstop, averagetpdatstop)
		totaltripsatallstops += averagetpdatstop
		munistops_dict[stop_id] = [stop_lat, stop_lon, averagetpdatstop]
		count += 1
		#print count, fileinlines, averagetpdatstop, maxaveragetpdatstop, totaltripsatallstops
		sline = filein.readline()
	print('count, fileinlines, averagetpdatstop, maxaveragetpdatstop, totaltripsatallstops')
	print(count, fileinlines, averagetpdatstop, maxaveragetpdatstop, totaltripsatallstops)
	print('------------------')
	print('stops lines scanned ', count)
	filein.close()

	# >>> load city boarders 
	with open(pathin / cityfilein) as cf:
		city_geo = json.load(cf)
	print('loaded city geo, feature count: ', len(city_geo['features']))
	#print city_geo

	# >>> load town boarders 
	with open(pathin / townfilein) as tf:
		town_geo = json.load(tf)
	print('loaded town geo, feature count: ', len(town_geo['features']))
	#print town_geo

	#
	# process loaded files
	#

	#
	# for each city and town 
	#   filter stops w tpd in boarders multipoly 
	#   sum the tpd from all stops in muni to get opd for muni
	#   output muni opd to txt file
	#

	fileout = open(pathout / munifileout, 'w', encoding="utf8") # open file to save results 
	postsline = 'municode,muni_name,opdinmuni,stopinmunicount\n'
	fileout.write(postsline)

	# for each city 
	for feature in city_geo['features']:
	# get muni boarders multipoly to use as filter
		#print feature['properties']
		muni_id = feature['properties']['muni_id']
		muni_name = feature['properties']['muni_name']
		print(muni_name)
		muni_boarder_multipoly = shape(feature['geometry']) # get muni boarders multipoly to use as filter
		#print len(feature['geometry']['coordinates']), muni_boarder_multipoly.geom_type
		#print feature['geometry']['coordinates'][0][0][0]
		if not muni_boarder_multipoly.is_valid : 
			muni_boarder_multipoly = muni_boarder_multipoly.buffer(0) # clean multipoly if not valid
			print('cleaned multipoly')

	# filter stops w tpd per line in boarders multipoly 
		muni_stops_dict = {}
		stopinmunicount = 0
		opdinmuni = 0.0
		for stop_id, [stop_lat, stop_lon, averagetpdatstop] in munistops_dict.items() :
			stop_loc = Point(float(stop_lon), float(stop_lat))
			if muni_boarder_multipoly.contains(stop_loc) :
			#print stop_loc
				stopinmunicount +=1

	# sum tpd per stop in muni to get opd
				opdinmuni += averagetpdatstop

		print('stopinmunicount, opdinmuni: ', stopinmunicount, round(opdinmuni))
		#print muni_tpdperline_dict

	# output muni opportunities per day (opd) to txt file
		postsline = muni_id+','+muni_name+','+str(round(opdinmuni))+','+str(stopinmunicount)+'\n' 
		fileout.write(postsline)

	# for each town 
	for feature in town_geo['features']:
	# get muni boarders multipoly to use as filter
		#print feature['properties']
		muni_id = feature['properties']['muni_id']
		muni_name = feature['properties']['muni_name']
		print(muni_name)
		muni_boarder_multipoly = shape(feature['geometry']) # get muni boarders multipoly to use as filter
		#print len(feature['geometry']['coordinates']), muni_boarder_multipoly.geom_type
		#print feature['geometry']['coordinates'][0][0][0]
		if not muni_boarder_multipoly.is_valid : 
			muni_boarder_multipoly = muni_boarder_multipoly.buffer(0) # clean multipoly if not valid
			print('cleaned multipoly')

	# filter stops w tpd per line in boarders multipoly 
		muni_stops_dict = {}
		stopinmunicount = 0
		opdinmuni = 0.0
		for stop_id, [stop_lat, stop_lon, averagetpdatstop] in munistops_dict.items() :
			stop_loc = Point(float(stop_lon), float(stop_lat))
			if muni_boarder_multipoly.contains(stop_loc) :
			#print stop_loc
				stopinmunicount +=1

	# sum tpd per stop in muni to get opd
				opdinmuni += averagetpdatstop

		print('stopinmunicount, opdinmuni: ', stopinmunicount, round(opdinmuni))
		#print muni_tpdperline_dict

	# output muni opportunities per day (opd) to txt file
		postsline = muni_id+','+muni_name+','+str(round(opdinmuni))+','+str(stopinmunicount)+'\n' 
		fileout.write(postsline)

	fileout.close()
	print('closed file: ', munifileout)


