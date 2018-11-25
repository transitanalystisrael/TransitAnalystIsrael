#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# scan stops.txt to create stops list with stop_id and location (lat, lon)
# output stops_gtfsdate.js 
#
import time
import csv
import json
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#

# input:
parent_path = 'C:\\transitanalyst\\gtfs\\'
pathout = 'C:\\transitanalyst\\processed\\'
gtfsdate = '20180425'
gtfsdir = 'israel'+gtfsdate
txtfilein = 'stops.txt'

# output:
jsfileout  = 'stops'+'_'+gtfsdate+'.js'

gtfspathin = parent_path+gtfsdir+'\\'
gtfspath = gtfspathin
gtfspathout = pathout

# >>> load stops file
stops_list = []
with open(gtfspathin+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'zone_id']
	print header
	for row in reader:
		#print row
		stops_list.append([row[0], row[1], row[2], row[3], float(row[4]), float(row[5]), row[6], row[7], row[8]])
print stops_list[0]
print 'stops_list loaded. stop count ', len(stops_list)

# ************************************************************************************************************************
# open and output js file 
#
'''
print ("Saving file: " + gtfspathout+jsfileout+ " ...")
nf = open(gtfspathout+jsfileout, "w")
outstr = 'var gtfsStops = {\n'
for [stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type, parent_station, zone_id] in stops_list :
	nf.write(outstr)
	if '/' in stop_name : stop_name = stop_name[:stop_name.find('/')]
	outstr = stop_id+': "'+stop_name+'",\n'
outstr = outstr[:-2]+'\n}'
nf.write(outstr)
nf.close()
print ("Saved file: " + jsfileout)
'''

def getJSON(s_id, s_lat, s_lon):
	return {
		"type": "Feature",
		"geometry": {
			"type": "Point",
			"coordinates": [float(s_lon),float(s_lat)]
		},
		"properties": { 
			"stop_id": s_id
		}
	}

# saveGeoJSON

print ("Generating GeoJSON export.")
geoj = {
	"type": "FeatureCollection",
	"features": [getJSON(stop_id, stop_lat, stop_lon) for [stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type, parent_station, zone_id] in stops_list]
}
print ("Saving file: " + gtfspathout+jsfileout+ " ...")
nf = open(gtfspathout+jsfileout, "w")
jsonstr = json.dumps(geoj, separators=(',',':')) # smaller file for download
outstr = jsonstr.replace('}},', '}},\n')
nf.write('var gtfsStops =\n')
nf.write(outstr)
nf.close()
print ("Saved file: " + jsfileout)

print "Local current time :", time.asctime( time.localtime(time.time()) )

