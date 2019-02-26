#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# for each muni, filter stops in muni to create stopsinmuni dict.
# output stops in muni in pre edit files both txt and js
# in order to allow manual editing of stops in muni in map based app
# also enables manual renaming txt output file from pre to post to bypass the editor
#
#
print('----------------- create files with stops in muni --------------------------')

from datetime import date
from datetime import timedelta
import time
import copy
import csv
import json
from shapely.geometry import shape, Point, Polygon, MultiPolygon
import numpy as np
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#_________________________________
#
def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
	# input:
	parent_path = pathout
	gtfs_parent_path = gtfsparentpath
	servicedate = gtfsdate
	gtfsdir = gtfsdirbase+servicedate+'\\'
	gtfsstopsfile = 'stops.txt'
	cityfilein = 'israel_city_boarders.geojson'
	townfilein = 'israel_town_boarders.geojson' # moatzot mekomiyot

	# output:
	stopsinmuni_pre_edit = 'stopsinmuni_pre_edit'+'_'+servicedate+'.js'
	stopsinmuni_pre_edit_txt = 'stopsinmuni_pre_edit'+'_'+servicedate+'.txt'

	gtfspathin = parent_path
	gtfspathout = parent_path

	#
	# load files 
	#

	# >>> load stops file
	txtfilein = gtfs_parent_path+gtfsdir+gtfsstopsfile
	stops_list = []
	with open(txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'zone_id']
		print(header)
		for row in reader:
			#print row
			stops_list.append([row[0], row[1], row[2], row[3], float(row[4]), float(row[5]), row[6], row[7], row[8]])
	print(stops_list[0])
	print('stops_list loaded. stop count ', len(stops_list))

	# >>> load city boarders 
	with open(parent_path+cityfilein) as cf:
		city_geo = json.load(cf)
	print('loaded city geo, feature count: ', len(city_geo['features']))
	#print city_geo

	# >>> load town boarders 
	with open(parent_path+townfilein) as tf:
		town_geo = json.load(tf)
	print('loaded town geo, feature count: ', len(town_geo['features']))
	#print town_geo

	#
	# process loaded files
	#

	#
	# create stop dict 
	#
	stops_dict = {}
	for [stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type, parent_station, zone_id] in stops_list:
		stops_dict[stop_id] = [float(stop_lat), float(stop_lon)]
	print('len(stops_dict) : ', len(stops_dict))


	#
	# for each city and town 
	#   filter stops in boarders multipoly 
	#

	munisforoutput_dict = {}
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

	# filter stops in boarders multipoly 

		stopinmunicount = 0
		for stop_id, [stop_lat, stop_lon] in stops_dict.items() :
			stop_loc = Point(stop_lon, stop_lat)
			if muni_boarder_multipoly.contains(stop_loc) :
				if muni_id in munisforoutput_dict:
					munisforoutput_dict[muni_id].append(stop_id)
				else :
					munisforoutput_dict[muni_id] = [stop_id]
				#print stop_loc
				stopinmunicount +=1
	print('len(munisforoutput_dict) with cities: ', len(munisforoutput_dict))
	print(munisforoutput_dict[muni_id]) # last one
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

	# filter stops in boarders multipoly 

		stopinmunicount = 0
		for stop_id, [stop_lat, stop_lon] in stops_dict.items() :
			stop_loc = Point(stop_lon, stop_lat)
			if muni_boarder_multipoly.contains(stop_loc) :
				if muni_id in munisforoutput_dict:
					munisforoutput_dict[muni_id].append(stop_id)
				else :
					munisforoutput_dict[muni_id] = [stop_id]
				#print stop_loc
				stopinmunicount +=1
	print('len(munisforoutput_dict) with cities and towns: ', len(munisforoutput_dict))
	print(munisforoutput_dict[muni_id]) # last one

	# output js file of stopsinmuni pre edit
	fileoutname = stopsinmuni_pre_edit
	fileout = open(gtfspathout+fileoutname, 'w', encoding="utf8") # open file to save results 
	postsline = 'var inmunis = {\n'
	for muni_id, stopsinmunilist in munisforoutput_dict.items():
		postsline += muni_id+': ["'
		for stop_id in stopsinmunilist :
			postsline += stop_id+'","'
		postsline = postsline[:-2]
		postsline += '],\n'
	postsline = postsline[:-2]
	postsline += '\n}'
	fileout.write(postsline)
	fileout.close()
	print('closed file: ', fileoutname)

	# output txt file of stopsinmuni pre edit
	fileoutname = stopsinmuni_pre_edit_txt
	fileout = open(gtfspathout+fileoutname, 'w', encoding="utf8") # open file to save results 
	postsline = 'muni_id,stop_id\n'
	fileout.write(postsline)
	for muni_id, stopsinmunilist in munisforoutput_dict.items():
		for stop_id in stopsinmunilist :
			postsline = muni_id+','+stop_id+'\n'
			fileout.write(postsline)
	fileout.close()
	print('closed file: ', fileoutname)

	print("Local current time :", time.asctime( time.localtime(time.time()) ))
