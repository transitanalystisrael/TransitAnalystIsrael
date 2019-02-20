#!/usr/bin/env python
#--------------------------------------------------
# Geo filter GTFS for all of Israel based on given list of train station locations
# input trainstops txt file with ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
# input GTFS dir israelyyyymmdd is expected in transitanalyst\\gtfs directory and as a command line argument 
# output per train station - GTFS dir 'israelyyyymmdd'+'_'+str(c_lat)+'_'+str(c_lon)+'_'+str(r)+'\\' will be created in transitanalyst\\processed
# need to set radius of circle below
#------------------------------------------------------------------------------------------
#----------------------------------------------------
# filter the GTFS files by a given area polygon
#--------------------------------------------------
import GTFS_geo_filter_full_circle
import os
import sys
import csv
#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)
print '# input GTFS dir israelyyyymmdd is expected in transitanalyst\\gtfs directory and as a command line argument '

parent_path = 'C:\\transitanalyst\\'
os.chdir(parent_path) # Changing the directory
print os.getcwd()

if len(sys.argv) > 1 :
	gtfsdir = str(sys.argv[1])
else :
	gtfsdir = 'israelyyyymmdd'
gtfspathin = parent_path + 'gtfs\\'+gtfsdir+'\\'
#***********************************************************************
# to enter input: change circle radius below
#***********************************************************************
r = 500.0 # meters
#*************************************************************************

# load trainstop file and loop for each trainstop



# >>> load trainstops txt file 
gtfsdate = gtfsdir[len('israel'):] # e.g '20180425'
print 'gtfsdate : ', gtfsdate
trainstopsfilein = 'train_stops'+'_'+gtfsdate+'.txt'
txtfilein = trainstopsfilein
trainstops_list = []
with open(parent_path+'processed\\'+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
	print header
	for row in reader:
		#print row
		trainstops_list.append([row[0], row[1], float(row[2]), float(row[3])])
print trainstops_list[:4]
print 'trainstops_list loaded. stop count ', len(trainstops_list)


for [stop_id, stop_name, stop_lat, stop_lon] in trainstops_list :
	gtfs_area_dir = gtfsdir+'_'+str(stop_lat)[:8]+'_'+str(stop_lon)[:8]+'_'+str(int(r))
	gtfspathout = parent_path+'processed\\'+gtfs_area_dir+'\\'
	if not os.access('processed\\'+gtfs_area_dir, os.F_OK): os.mkdir('processed\\'+gtfs_area_dir)
	GTFS_geo_filter_full_circle.main(gtfspathin, gtfspathout, stop_lat, stop_lon, r)
	print 'gtfspathin, gtfspathout, lat, lon, r : ', gtfspathin, gtfspathout, stop_lat, stop_lon, r
	print 'filter done for ', stop_name


