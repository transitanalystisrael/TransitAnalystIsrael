#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create txt file with tpd per line (agency_id+route_short_name) at stop 
#
# input:
#   parent_path = 'C:\\transitanalyst\\processed\\'
#   servicedate = '20180425'
#   geojson file of stops with max and average trips per day and tpd per line (agency_id+route_short_name) -'stops_w_tpd_per_line'+'_'+servicedate+'.geojson'
#
# output:
#   txt file with tpd per line (agency_id+route_short_name) at stop - 'stops_w_tpd_per_line'+'_'+servicedate+'.txt'
#
print '----------------- create txt file with tpd per line (agency_id+route_short_name) at stop --------------------------'
print 'output txt file with tpd per line (agency_id+route_short_name) at stop'
from datetime import date
from datetime import timedelta
import time
import copy
import csv
import json
print "Local current time :", time.asctime( time.localtime(time.time()) )
#_________________________________
#
# input:
parent_path = 'C:\\transitanalyst\\processed\\'
servicedate = '20180425'
stopswtpdfile = 'stops_w_tpd_per_line'+'_'+servicedate+'.geojson'

# output:
stopswtpdtxtfile = 'stops_w_tpd_per_line'+'_'+servicedate+'.txt'


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

#
# for each trainstop 
#   output stop tpd per line dict to txt file
#

fileout = open(gtfspathout+stopswtpdtxtfile, 'w') # open file to save results 
postsline = 'stop_id,stop_lat,stop_lon,maxtpdatstop,averagetpdatstop,line_name,linetpdatstop\n' 
fileout.write(postsline)

stopcount = 0
linesatstop = len(maxdaytpdperline_dict)
for stop_id, [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict] in stops_dict.iteritems() :
	stopcount +=1
	#print maxdaytpdperline_dict
	for line_name, linetpdatstop in maxdaytpdperline_dict.iteritems() :
		clean_line_name = ''
		for i in range(len(line_name)): # stupid workaround for unicode problem of aleph in route_short_name
			lnchar = line_name[i]
			if lnchar == '-' : lnchar = '-'
			elif lnchar > '9': lnchar = 'a'
			clean_line_name += lnchar
		line_name = clean_line_name
		#print line_name

		# output to txt file

		postslinelist = [stop_id,str(stop_lat),str(stop_lon),str(maxtpdatstop),str(averagetpdatstop),line_name,str(linetpdatstop)]
		postsline = ','.join(postslinelist) + '\n'
		fileout.write(postsline)

print 'stopcount : ', stopcount

fileout.close()
print 'closed file: ', stopswtpdtxtfile





