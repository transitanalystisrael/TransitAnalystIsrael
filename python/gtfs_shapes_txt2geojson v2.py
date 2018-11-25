#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert a GTFS shapes.txt file to a geojson file of linestring shapes
#
# inputs:
#   parent_path = 'C:\\transitanalyst\\processed\\'
#   gtfsdir = 'israel20180106-binyamina_station'
#
# outputs:
#   output geojson file of shape geometry - 'shapes_'+gtfsdir+'.geojson'
#
print '----------------- convert a GTFS shapes.txt file to a geojson file --------------------------'

#from datetime import date
#from datetime import timedelta
import time
#import copy
import json
#from operator import itemgetter
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
parent_path = 'C:\\transitanalyst\\processed\\'
gtfsdir = 'israel20180425_israel-mahoz_tel_aviv'
geojson_file_name = 'shapes_'+gtfsdir+'.geojson'

gtfspathin = parent_path+gtfsdir+'\\'
gtfspath = gtfspathin
gtfspathout = parent_path

MAX_STOPS_COUNT = 50000
MAX_STOP_TIMES_COUNT = 25000000
MAX_TRIPS_COUNT = 900000
MAX_SHAPES_COUNT = 10000000
MAX_ROUTES_COUNT = 15000
MAX_AGENCY_COUNT = 100
MAX_CALENDAR_COUNT = 250000

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
#print shapes_dict

#
# output geojson file of shapes with shape geometry
#

def getJSON(s_id):
	print s_id
	print shapes_dict[s_id][:3]
	#print routeswshape_dict[r_id]
	#print routeswshape_dict[r_id][4]
	return {
		"type": "Feature",
		"geometry": {
			"type": "LineString",
			"coordinates": [[round(float(shape_pt_lon),5), round(float(shape_pt_lat),5)] for [shape_pt_lat, shape_pt_lon, shape_pt_sequence] in shapes_dict[s_id]] 
		},
		"properties": { 
			"shape_id": s_id,
			"shape_len": len(shapes_dict[s_id])
			#"agency_id": unique_route_dict[r_id][0],
			#"agency_name": agency_dict[unique_route_dict[r_id][0]],
			#"route_short_name": unique_route_dict[r_id][1],
			#"totaltripsperroute": unique_route_dict[r_id][2],
			#"maxtpdperroute": unique_route_dict[r_id][3] 
			}
	}

# saveGeoJSON
print ("Generating GeoJSON export.")

geoj = {
	"type": "FeatureCollection",
	"features": [getJSON(shape_id) for shape_id in shapes_dict]
}
print ("Saving file: " + gtfspathout+geojson_file_name + " ...")
nf = open(gtfspathout+geojson_file_name, "w")
json.dump(geoj, nf, separators=(',',':'))
nf.close()
print ("Saved file: " + geojson_file_name)

