#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# scan stops.txt to create stops list with stop_id, stop name and location (lat, lon)
# output train_stops_gtfsdate.txt 
# output train_stops_gtfsdate.js 
#
import time
import csv
from geopy.distance import vincenty
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#

# input:
parent_path = 'C:\\transitanalyst\\gtfs\\'
pathout = 'C:\\transitanalyst\\processed\\'
gtfsdate = '20181021'
gtfsdir = 'israel'+gtfsdate
txtfilein = 'stops.txt'

# output:
txtfileout = 'train_stops'+'_'+gtfsdate+'.txt'
jsfileout  = 'train_stops'+'_'+gtfsdate+'.js'

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
		stops_list.append([row[0], row[2], row[3], float(row[4]), float(row[5])])
print stops_list[:4]
print 'stops_list loaded. stop count ', len(stops_list)

#collect all train stops
all_train_stops_list = []
for [stop_id, stop_name, stop_desc, stop_lat, stop_lon] in stops_list :
	train_stop = ('ת. רכבת' in (stop_name+stop_desc) or 'תחנת רכבת' in (stop_name+stop_desc))and ('קלה' not in (stop_name+stop_desc))
	if train_stop :
		all_train_stops_list.append([stop_id, stop_name, stop_lat, stop_lon])
		print stop_name
#print all_train_stops_list
print 'all_train_stops_list created. stop count ', len(all_train_stops_list)

# merge stops that are in same location (less than 500m apart)
train_stops_list = []
train_stops_list.append(all_train_stops_list[0])
for [stop_id, stop_name, stop_lat, stop_lon] in all_train_stops_list :
	same_location = False
	for i, [stop_id1, stop_name1, stop_lat1, stop_lon1] in enumerate(train_stops_list) :
		stop_loc = (stop_lat, stop_lon)
		stop_loc1 = (stop_lat1, stop_lon1)
		distance = vincenty(stop_loc,stop_loc1).m
		if distance < 500.0 : 
			same_location = True
			print i, distance
			same_stop_lat = (stop_lat+stop_lat1)/2
			same_stop_lon = (stop_lon+stop_lon1)/2
			same_i = i
	if not same_location :
		train_stops_list.append([stop_id, stop_name, stop_lat, stop_lon])
		#print stop_name
	else : # same location so update stop loc with average stop loc
		train_stops_list[same_i][2] = same_stop_lat
		train_stops_list[same_i][3] = same_stop_lon
#print all_train_stops_list
print 'all_train_stops_list created. stop count ', len(all_train_stops_list)

# ************************************************************************************************************************
# open and prep output txt file 
#
print 'open file ', pathout+txtfileout
fileout = open(pathout+txtfileout, 'w') # save results in file
postsline = 'stop_id,stop_name,stop_lat,stop_lon\n'
print postsline
fileout.write(postsline)
outfilelinecount = 0

for [stop_id, stop_name, stop_lat, stop_lon] in train_stops_list :
	if '/' in stop_name : stop_name = stop_name[:stop_name.find('/')]
	postsline = ','.join([stop_id, stop_name, str(stop_lat), str(stop_lon)])+'\n'
	fileout.write(postsline)
	outfilelinecount += 1
fileout.close()
print 'close file ', pathout+txtfileout
print 'lines in out file count ', outfilelinecount

# ************************************************************************************************************************
# open and output js file 
#
print ("Saving file: " + gtfspathout+jsfileout+ " ...")
nf = open(gtfspathout+jsfileout, "w")
outstr = 'var trainstopsName = {\n'
for [stop_id, stop_name, stop_lat, stop_lon] in train_stops_list :
	nf.write(outstr)
	if '/' in stop_name : stop_name = stop_name[:stop_name.find('/')]
	outstr = stop_id+': "'+stop_name+'",\n'
outstr = outstr[:-2]+'\n}'
nf.write(outstr)
nf.close()
print ("Saved file: " + jsfileout)

print "Local current time :", time.asctime( time.localtime(time.time()) )

