#!/usr/bin/env python
# -*- coding: utf-8 -*-
# calculate the change of trips per day at all stops from servicedate0 to servicedate1
# include breakdown of change in tpd per line (route short name) at each stop
#
# inputs:
#   parent_path = 'C:\\transitanalyst\\processed\\'
#   servicedate0 = '20170108'
#   servicedate1 = '20180425'
#   1st geojson file of stops with max and average trips per day and tpd per line (route short name) -'stops_w_tpd_per_line'+'_'+servicedate0+'.geojson'
#   2nd geojson file of stops with max and average trips per day and tpd per line (route short name) -'stops_w_tpd_per_line'+'_'+servicedate1+'.geojson'
#
# outputs:
#   geojson file of stops with delta of max and average tpd and tpd per line (route short name) -'stops_w_delta_tpd_per_line'+'_'+servicedate0+'_'+servicedate1+'.geojson'
#
print '----------------- calculate the change of trips per day at all stops from servicedate0 to servicedate1 --------------------------'
print 'output geojson file of stops with delta of max and average tpd and tpd per line (route short name)'
from datetime import date
from datetime import timedelta
import time
import copy
import json
print "Local current time :", time.asctime( time.localtime(time.time()) )
#_________________________________
#
parent_path = 'C:\\transitanalyst\\processed\\'
servicedate0 = '20170108'
servicedate1 = '20180425'
stopswtpdfile0 = 'stops_w_tpd_per_line'+'_'+servicedate0+'.geojson'
stopswtpdfile1 = 'stops_w_tpd_per_line'+'_'+servicedate1+'.geojson'
stopswdeltatpdfile = 'stops_w_delta_tpd_per_line'+'_'+servicedate0+'_'+servicedate1+'.geojson'

gtfspathin = parent_path
gtfspathout = parent_path

#
# load files 
#

# >>> load 1st stops_w_tpd_per_line geojson file 
with open(parent_path+stopswtpdfile0) as sf0:
	stops_geo0 = json.load(sf0)
print 'loaded stops_geo0, feature count: ', len(stops_geo0['features'])
#print stops_geo0

# >>> load 2nd stops_w_tpd_per_line geojson file 
with open(parent_path+stopswtpdfile1) as sf1:
	stops_geo1 = json.load(sf1)
print 'loaded stops_geo1, feature count: ', len(stops_geo1['features'])
#print stops_geo1

#
# collect set of all stop_ids - do not assume that stops have not changed...
# recreate stop dicts 
#
stop_id_set = set({})
stops_dict0 = {}
stops_dict1 = {}

for feature in stops_geo0['features']:
	#print feature['geometry']
	#print feature['properties']
	stop_id = feature['properties']['stop_id']
	stop_lat = feature['geometry']['coordinates'][1]
	stop_lon = feature['geometry']['coordinates'][0]
	maxtpdatstop = feature['properties']['maxtpdatstop']
	averagetpdatstop = feature['properties']['averagetpdatstop']
	maxdaytpdperline_dict = feature['properties']['maxdaytpdperline_dict']
	
	stop_id_set.add(stop_id)
	stops_dict0[stop_id] = [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
print 'len(stop_id_set) : ', len(stop_id_set)

for feature in stops_geo1['features']:
	#print feature['geometry']
	#print feature['properties']
	stop_id = feature['properties']['stop_id']
	stop_lat = feature['geometry']['coordinates'][1]
	stop_lon = feature['geometry']['coordinates'][0]
	maxtpdatstop = feature['properties']['maxtpdatstop']
	averagetpdatstop = feature['properties']['averagetpdatstop']
	maxdaytpdperline_dict = feature['properties']['maxdaytpdperline_dict']
	
	stop_id_set.add(stop_id)
	stops_dict1[stop_id] = [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
print 'len(stop_id_set) : ', len(stop_id_set)

#
# count changes in stops
#
count_ff = 0
count_ft = 0
count_tf = 0
count_tt = 0
for stop_id in stop_id_set :
	#print stop_id, stop_id in stops_dict0, stop_id in stops_dict1
	if stop_id not in stops_dict0 and stop_id not in stops_dict1 : count_ff +=1
	if stop_id in stops_dict0 and stop_id not in stops_dict1 : count_ft +=1
	if stop_id not in stops_dict0 and stop_id in stops_dict1 : count_tf +=1
	if stop_id in stops_dict0 and stop_id in stops_dict1 : count_tt +=1
	
print 'count_ff, count_ft, count_tf, count_tt'
print count_ff, count_ft, count_tf, count_tt

#
# create stops dict with delta info
#
def negtpdperline(tpdperline_dict):
	out_dict = {}
	#print tpdperline_dict
	for line_name, tpdperline in tpdperline_dict.iteritems(): 
		#print line_name
		out_dict[line_name] = -tpdperline
	#print out_dict
	return out_dict

def deltatpdperline(tpdperline_dict0, tpdperline_dict1):
	out_dict = {}
	line_name_set = set({})
	#print tpdperline_dict0
	#print tpdperline_dict1
	for line_name, tpdperline in tpdperline_dict0.iteritems(): line_name_set.add(line_name)
	for line_name, tpdperline in tpdperline_dict1.iteritems(): line_name_set.add(line_name)
	for line_name in line_name_set :
		if line_name not in tpdperline_dict0 and line_name not in tpdperline_dict1 : print '***************************error***************************'
		if line_name in tpdperline_dict0 and line_name not in tpdperline_dict1 : out_dict[line_name] = -tpdperline_dict0[line_name]
		if line_name not in tpdperline_dict0 and line_name in tpdperline_dict1 : out_dict[line_name] = tpdperline_dict1[line_name]
		if line_name in tpdperline_dict0 and line_name in tpdperline_dict1 : out_dict[line_name] = tpdperline_dict1[line_name]-tpdperline_dict0[line_name]
	#print out_dict
	return out_dict

stopmovedcount = 0
stops_delta_dict = {}
for stop_id in stop_id_set :
	if stop_id in stops_dict0 and stop_id not in stops_dict1 : 
		stops_delta_dict[stop_id] = [
			stops_dict0[stop_id][0],
			stops_dict0[stop_id][1],
			-stops_dict0[stop_id][2],
			-stops_dict0[stop_id][3],
			negtpdperline(stops_dict0[stop_id][4])
		]
	if stop_id not in stops_dict0 and stop_id in stops_dict1 : 
		stops_delta_dict[stop_id] = stops_dict1[stop_id]
	if stop_id in stops_dict0 and stop_id in stops_dict1 : 
		if (stops_dict0[stop_id][0] - stops_dict1[stop_id][0] > 0.001) or (stops_dict0[stop_id][1] - stops_dict1[stop_id][1] > 0.001) : 
			print '******* stop moved *****************'
			stopmovedcount +=1
			print stopmovedcount, stop_id, stops_dict0[stop_id][0], stops_dict1[stop_id][0], stops_dict0[stop_id][1], stops_dict1[stop_id][1]
		stops_delta_dict[stop_id] = [
			stops_dict1[stop_id][0],
			stops_dict1[stop_id][1],
			stops_dict1[stop_id][2]-stops_dict0[stop_id][2],
			stops_dict1[stop_id][3]-stops_dict0[stop_id][3],
			deltatpdperline(stops_dict0[stop_id][4],stops_dict1[stop_id][4])
		]
#
# output geojson file of stops with delta of max and average tpd and tpd per line (route short name) -'stops_w_delta_tpd_per_line'+'_'+servicedate0+'_'+servicedate1+'.geojson'
#

def getJSON(s_id):
	return {
		"type": "Feature",
		"geometry": {
			"type": "Point",
			"coordinates": [float(stops_delta_dict[s_id][1]),float(stops_delta_dict[s_id][0])]
		},
		"properties": { 
			"stop_id": s_id,
			"maxtpdatstop": stops_delta_dict[s_id][2],
			"averagetpdatstop": stops_delta_dict[s_id][3],
			"maxdaytpdperline_dict": stops_delta_dict[s_id][4]
		}
	}

# saveGeoJSON
print ("Generating GeoJSON export.")
geojson_file_name = stopswdeltatpdfile
geoj = {
	"type": "FeatureCollection",
	"features": [getJSON(stop_id) for stop_id in stops_delta_dict]
}
print ("Saving file: " + gtfspathout+geojson_file_name + " ...")
nf = open(gtfspathout+geojson_file_name, "w")
#json.dump(geoj, nf, indent=4) # more readable file
json.dump(geoj, nf) # smaller file for download
nf.close()
print ("Saved file: " + geojson_file_name)


