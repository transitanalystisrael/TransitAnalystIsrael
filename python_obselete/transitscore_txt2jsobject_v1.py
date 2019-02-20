#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# convert transitscore txt grid file - transit_score_yyyymmdd.txt - to js object with gridlatlon as key to look up transitscore property from 1-100 
# output ts_lookup.js
#
print '----------------- convert grid file to object with key gridlatlon to look up transitscore --------------------------'
print 'convert transitscore txt grid file - transit_score_all_israel.txt - to js object with gridlatlon as key to look up transitscore property from 1-100 '
print 'output ts_lookup.js'

import time
import csv
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
def main(gtfsdate, gtfsdirbase, processedpath):
	parent_path = processedpath

	tsfilein = 'transit_score_'+gtfsdirbase+gtfsdate+'.txt'
	tsfileout = 'ts_lookup_'+gtfsdirbase+gtfsdate+'.js'

	ilminlat = 29.490000 # Israel min lat
	ilminlon = 34.280000 # Israel min lon

	#
	# load file
	#

	# >>> load transitscore file
	transitscore_list = []
	max_grid_lat = 0
	max_grid_lon = 0
	with open(parent_path+tsfilein, 'rb') as ts_f:
		readerts = csv.reader(ts_f)
		headerts = readerts.next()
		print headerts
		for row in readerts:
			#print row
			grid_lat = int(row[0])
			grid_lon = int(row[1])
			ts = int(float(row[2]))
			max_grid_lat = max(max_grid_lat, grid_lat)
			max_grid_lon = max(max_grid_lon, grid_lon)
			transitscore_list.append([grid_lat, grid_lon, ts])
	#print transitscore_list
	print 'transitscore_list loaded. ts count ', len(transitscore_list)
	print 'max_grid_lat, max_grid_lon : ', max_grid_lat, max_grid_lon

	#
	# output file of ts_lookup as object with gridlatlon as key to look up transitscore from 1-100
	#
	print ("Saving file: " + parent_path+tsfileout + " ...")
	nf = open(parent_path+tsfileout, "w")
	postsline = 'var transitScore = {\n' # format as js for load to leaflet
	print postsline
	nf.write(postsline)

	i=0
	grid_lat = 0
	grid_lon = 0
	ts = 0
	gridlatlon = 10000*grid_lat+grid_lon
	postsline = str(gridlatlon)+':'+str(ts)
	print postsline
	nf.write(postsline)

	for [grid_lat, grid_lon, ts] in transitscore_list :
		gridlatlon = 10000*grid_lat+grid_lon
		i += 1
		if i%100 == 0 :
			postsline = ','+str(gridlatlon)+':'+str(ts)+'\n'
			#print postsline
		else :
			postsline = ','+str(gridlatlon)+':'+str(ts)
		nf.write(postsline)
		
	postsline = '\n};'
	nf.write(postsline)
	nf.close()
	print ("Saved file: " + tsfileout)
