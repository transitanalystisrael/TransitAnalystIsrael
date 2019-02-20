#!/usr/bin/env python
# -*- coding: utf-8 -*-

# create stops js file with location and tpdperline and trainstop ids if near trainstop
#

print '----------------- create stops js file with location and tpdperline and trainstop ids if near trainstop --------------------------'

from datetime import date
from datetime import timedelta
import time
import copy
import csv
import json
from geopy.distance import vincenty
import numpy as np
print "Local current time :", time.asctime( time.localtime(time.time()) )
#_________________________________
#
def main(gtfsdate, processedpath):
	# input:
	parent_path = processedpath
	servicedate = gtfsdate
	stopswtpdfile = 'stops_w_tpd_per_line'+'_'+servicedate+'.geojson'
	stopsneartrainstop_post_edit = 'stopsneartrainstop_post_edit'+'_'+servicedate+'.txt'
	# output:
	stopswtrainstopids = 'stopswtrainstopids'+'_'+servicedate+'.js'

	gtfspathin = parent_path
	gtfspathout = parent_path

	#
	# load files 
	#

	# >>> load stops_w_tpd_per_line geojson file 
	print parent_path+stopswtpdfile
	with open(parent_path+stopswtpdfile) as sf:
		stops_geo = json.load(sf)
	print 'loaded stops_geo, feature count: ', len(stops_geo['features'])
	#print stops_geo

	# >>> load txt file of stopsneartrainstop post edit
	txtfilein = stopsneartrainstop_post_edit
	stopsneartrainstop = {}
	with open(gtfspathin+txtfilein, 'rb') as f:
		reader = csv.reader(f)
		header = reader.next() # ['trainstop_id', 'stop_id']
		print header
		for row in reader:
			#print row
			trainstop_id = row[0]
			stop_id = row[1]
			if trainstop_id in stopsneartrainstop :
				stopsneartrainstop[trainstop_id].append(stop_id)
			else :
				stopsneartrainstop[trainstop_id] = [stop_id]
	print stopsneartrainstop[trainstop_id] # last one
	print 'stopsneartrainstop loaded. trainstop count ', len(stopsneartrainstop)

	#
	# process loaded files
	#

	#
	# recreate stop dict 
	#
	stops_dict = {}
	for feature in stops_geo['features']:
		#print feature['geometry']
		#print feature['properties']
		stop_id = feature['properties']['stop_id']
		stop_lat = feature['geometry']['coordinates'][1]
		stop_lon = feature['geometry']['coordinates'][0]
		maxtpdatstop = feature['properties']['maxtpdatstop']
		averagetpdatstop = feature['properties']['averagetpdatstop']
		maxdaytpdperline_dict = feature['properties']['maxdaytpdperline_dict']
		
		stops_dict[stop_id] = [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
	print 'len(stops_dict) : ', len(stops_dict)

	#print stopsneartrainstop
	stopswtrainstopid_dict = {}
	for s_id, stopinfolist in stops_dict.iteritems():
		stopswtrainstopid_dict[s_id] = "0" # init trainstop id with with "0" - no trainstop near this stop
	# now loop through all trainstops and stops near each trainstop to enter trainstop_ids
	for ts_id, s_list in stopsneartrainstop.iteritems() : 
		#print ts_id, s_list
		for s_id in s_list :
			stopswtrainstopid_dict[s_id] = ts_id

	#
	#   output js file of stops with location stop_id and trainstop_id of near trainstop ("0" if none)
	#

	jsfileout = stopswtrainstopids

	def getJSON(s_id, s_lat, s_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict):
		return {
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": [float(s_lon),float(s_lat)]
			},
			"properties": { 
				"s_id": s_id,
				"ts_id": stopswtrainstopid_dict[s_id],
				"maxtpdatstop": maxtpdatstop, 
				"averagetpdatstop": averagetpdatstop, 
				"maxdaytpdperline_dict": maxdaytpdperline_dict
			}
		}

	# saveGeoJSON

	print ("Generating GeoJSON export.")
	geoj = {
		"type": "FeatureCollection",
		"features": [getJSON(stop_id, stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict) 
			for stop_id, [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict] in stops_dict.iteritems()]
	}
	print ("Saving file: " + gtfspathout+jsfileout+ " ...")
	nf = open(gtfspathout+jsfileout, "w")
	jsonstr = json.dumps(geoj, separators=(',',':')) # smaller file for download
	outstr = jsonstr.replace('}},', '}},\n')
	nf.write('var stopsWtrainstopid =\n')
	nf.write(outstr)
	nf.close()
	print ("Saved file: " + jsfileout)

	print "Local current time :", time.asctime( time.localtime(time.time()) )
