#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# for each TrainStop, filter stops near trainstop location to create stopsneartrainstop dict.
# output stops near trainstops in pre edit files both txt and js
# in order to allow manual editing of stops near trainstops in map based app
# also enables manual renaming txt output file from pre to post to bypass the editor
#
# note that "near" is set at 500 meters ... can be easily changed...
#
print '----------------- create files with stops near trainstop --------------------------'

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
# input:
parent_path = 'C:\\transitanalyst\\processed\\'
gtfs_parent_path = 'C:\\transitanalyst\\gtfs\\'
servicedate = '20181021'
gtfsdir = 'israel'+servicedate+'\\'
gtfsstopsfile = 'stops.txt'
trainstopsfilein = 'train_stops'+'_'+servicedate+'.txt'
NEAR = 500.0 # meters

# output:
stopsneartrainstop_pre_edit = 'stopsneartrainstop_pre_edit'+'_'+servicedate+'.js'
stopsneartrainstop_pre_edit_txt = 'stopsneartrainstop_pre_edit'+'_'+servicedate+'.txt'

gtfspathin = parent_path
gtfspathout = parent_path

#
# load files 
#

# >>> load stops file
txtfilein = gtfs_parent_path+gtfsdir+gtfsstopsfile
stops_list = []
with open(txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'zone_id']
	print header
	for row in reader:
		#print row
		stops_list.append([row[0], row[1], row[2], row[3], float(row[4]), float(row[5]), row[6], row[7], row[8]])
print stops_list[0]
print 'stops_list loaded. stop count ', len(stops_list)

# >>> load trainstops txt file 
txtfilein = trainstopsfilein
trainstops_list = []
with open(gtfspathin+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
	print header
	for row in reader:
		#print row
		trainstops_list.append([row[0], float(row[2]), float(row[3])])
print trainstops_list[:4]
print 'trainstops_list loaded. stop count ', len(trainstops_list)

#
# process loaded files
#

#
# create stop dict 
#
stops_dict = {}
for [stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type, parent_station, zone_id] in stops_list:
	stops_dict[stop_id] = [stop_lat, stop_lon]
print 'len(stops_dict) : ', len(stops_dict)

#
# for each trainstop 
#   filter stops near trainstop location to create stopsneartrainstop dict
trainstopcount = 0
stopsneartrainstop = {}
# for each trainstop
# get trainstop location to use as filter
for [trainstop_id, trainstop_lat, trainstop_lon] in trainstops_list:
	print trainstop_lat, trainstop_lon, trainstop_id
	trainstopcount +=1
	stopsneartrainstop[trainstop_id] = []
	trainstop_loc = (trainstop_lat, trainstop_lon)
# filter stops near trainstop
	stopneartrainstopcount = 0
	for stop_id, [stop_lat, stop_lon] in stops_dict.iteritems() :
		stop_loc = (stop_lat, stop_lon)
		distance = vincenty(stop_loc,trainstop_loc).m
		if distance < NEAR : 
			#print stop_loc
			stopneartrainstopcount +=1
			stopsneartrainstop[trainstop_id].append(stop_id)
	print 'trainstopcount, stopneartrainstopcount : ', trainstopcount, stopneartrainstopcount
print 'stopsneartrainstop[trainstop_id] - last one: ', stopsneartrainstop[trainstop_id] # last one

# output js file of stopsneartrainstop pre edit
fileoutname = stopsneartrainstop_pre_edit
fileout = open(gtfspathout+fileoutname, 'w') # open file to save results 
postsline = 'var nearTrainstops = {\n'
for trainstop_id, stopsnearlist in stopsneartrainstop.iteritems():
	postsline += trainstop_id+': ["'
	for stop_id in stopsnearlist :
		postsline += stop_id+'","'
	postsline = postsline[:-2]
	postsline += '],\n'
postsline = postsline[:-2]
postsline += '\n}'
fileout.write(postsline)
fileout.close()
print 'closed file: ', fileoutname

# output txt file of stopsneartrainstop pre edit
fileoutname = stopsneartrainstop_pre_edit_txt
fileout = open(gtfspathout+fileoutname, 'w') # open file to save results 
postsline = 'trainstop_id,stop_id\n'
fileout.write(postsline)
for trainstop_id, stopsnearlist in stopsneartrainstop.iteritems():
	for stop_id in stopsnearlist :
		postsline = trainstop_id+','+stop_id+'\n'
		fileout.write(postsline)
fileout.close()
print 'closed file: ', fileoutname

print "Local current time :", time.asctime( time.localtime(time.time()) )
