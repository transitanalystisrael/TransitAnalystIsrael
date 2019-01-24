#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create txt and js files with opportunities per day (opd) per line (agency_id+route_short_name) in muni 
# boarders are multipolygons with holes in some of the polygons 
# for each city and town, need to filter stops w tpd per line file and merge the count per line from all stops in muni
#
# input:
#   parent_path = 'C:\\transitanalyst\\processed\\'
#   servicedate = '20181021'
#   israel_city_boarders.geojson
#   israel_town_boarders.geojson # moatzot mekomiyot
#   geojson file of stops with max and average trips per day and tpd per line (agency_id+route_short_name) -'stops_w_tpd_per_line'+'_'+servicedate+'.geojson'
#
# output:
#   txt file with tpd per line (agency_id+route_short_name) in muni - 'muni_w_opd_per_line'+'_'+servicedate+'.txt'
#   js file with opd per line (agency_id+route_short_name) in muni - 'muni_w_opd_per_line'+'_'+servicedate+'.js'
#   txt file with stop_id and muni_id if stop in muni - stopstxtfileout = 'stopsinmuni'+'_'+servicedate+'.txt'
#
print '----------------- create txt and js files with opd per line (agency_id+route_short_name) in muni --------------------------'
print 'output txt and js files with opd per line (agency_id+route_short_name) in muni'
from datetime import date
from datetime import timedelta
import time
import copy
import json
from shapely.geometry import shape, Point, Polygon, MultiPolygon
import numpy as np
print "Local current time :", time.asctime( time.localtime(time.time()) )
#_________________________________
#
# input:
parent_path = 'C:\\transitanalyst\\processed\\'
servicedate = '20181021'
stopswtpdfile = 'stops_w_tpd_per_line'+'_'+servicedate+'.geojson'
cityfilein = 'israel_city_boarders.geojson'
townfilein = 'israel_town_boarders.geojson' # moatzot mekomiyot
# output:
txtfileout = 'muni_w_opd_per_line'+'_'+servicedate+'.txt'
jsfileout = 'muni_w_opd_per_line'+'_'+servicedate+'.js'
stopstxtfileout = 'stopsinmuni'+'_'+servicedate+'.txt'

gtfspathin = parent_path
gtfspathout = parent_path

#
# load files 
#

# >>> load stops_w_tpd_per_line geojson file 
with open(parent_path+stopswtpdfile) as sf:
	stops_geo = json.load(sf)
print 'loaded stops_geo, feature count: ', len(stops_geo['features'])
#print stops_geo

# >>> load city boarders 
with open(parent_path+cityfilein) as cf:
	city_geo = json.load(cf)
print 'loaded city geo, feature count: ', len(city_geo['features'])
#print city_geo

# >>> load town boarders 
with open(parent_path+townfilein) as tf:
	town_geo = json.load(tf)
print 'loaded town geo, feature count: ', len(town_geo['features'])
#print town_geo

#
# process loaded files
#

#
# recreate stop dict and initialize muni stops dict
#
muni_stops_dict = {}
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
	muni_stops_dict[stop_id] = '0' # initialize to muni_id = '0' = not in muni
print 'len(stops_dict) : ', len(stops_dict)

#
# for each city and town 
#   filter stops w tpd per line in boarders multipoly 
#   merge the tpd per line from all stops in muni
#   output merged muni tpd per line dict to txt file
#

fileout = open(gtfspathout+txtfileout, 'w') # open file to save results 
postsline = 'muni_id,line_name,opdinmuni,linestopsinmuni,averagetpdatstop,mediantpdatstop\n'
fileout.write(postsline)

munisforoutput_dict = {}
# for each city 
for feature in city_geo['features']:
# get muni boarders multipoly to use as filter
	#print feature['properties']
	muni_id = feature['properties']['muni_id']
	muni_name = feature['properties']['muni_name']
	print muni_name
	muni_boarder_multipoly = shape(feature['geometry']) # get muni boarders multipoly to use as filter
	#print len(feature['geometry']['coordinates']), muni_boarder_multipoly.geom_type
	#print feature['geometry']['coordinates'][0][0][0]
	if not muni_boarder_multipoly.is_valid : 
		muni_boarder_multipoly = muni_boarder_multipoly.buffer(0) # clean multipoly if not valid
		print 'cleaned multipoly'

# filter stops w tpd per line in boarders multipoly 

	muni_tpdperline_dict = {} # line_name:[totalopd,[tpd1,tpd2,tpd3...]]
	stopinmunicount = 0
	opdinmuni = 0
	linesinmuni = 0
	for stop_id, [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict] in stops_dict.iteritems() :
		stop_loc = Point(stop_lon, stop_lat)
		if muni_boarder_multipoly.contains(stop_loc) :
			muni_stops_dict[stop_id] = muni_id
			#print stop_loc
			stopinmunicount +=1


# merge the tpd per line from stop in muni
			#print maxdaytpdperline_dict
			for line_name, tpd in maxdaytpdperline_dict.iteritems() :
				clean_line_name = ''
				for i in range(len(line_name)): # stupid workaround for unicode problem of aleph in route_short_name
					lnchar = line_name[i]
					if lnchar == '-' : lnchar = '-'
					elif lnchar > '9': lnchar = 'a'
					clean_line_name += lnchar
				line_name = clean_line_name
				#print line_name
				opdinmuni += tpd
				if line_name not in muni_tpdperline_dict : # not in merged dict then add it
					#muni_tpdperline_dict[line_name] = tpd # merge by sum
					muni_tpdperline_dict[line_name] = [tpd,[tpd]] # merge by sum and collecting
					linesinmuni +=1
				else: # already in merged dict then sum tpd
					#muni_tpdperline_dict[line_name] += tpd # merge by sum
					muni_tpdperline_dict[line_name][0] += tpd # merge by sum
					muni_tpdperline_dict[line_name][1].append(tpd) # and merge by collecting
	print 'stopinmunicount, linesinmuni, opdinmuni: ', stopinmunicount, linesinmuni, opdinmuni
	#print muni_tpdperline_dict

# output merged muni opportunities per day (opd) per line dict to txt file
#   and collect munisforoutput_dict for js output
	total_muni_opd = 0
	total_muni_tpd = 0
	tpdperline_dict = {}
	munisforoutput_dict[muni_id] = [total_muni_opd, total_muni_tpd, tpdperline_dict] # collect muni_id and placeholders
	#for line_name, [opd,tpdlist] in muni_tpdperline_dict.iteritems() :
	for line_name, [opd,tpdlist] in sorted(muni_tpdperline_dict.iteritems(), reverse=True, key=lambda(k,v): (v[0]/len(v[1]))):
		averagetpdperline = opd/len(tpdlist)
		stopsperlineinmuni = len(tpdlist)
		mediantpdperline = int(np.median(np.array(tpdlist)))
		#postsline = muni_id+','+line_name+','+str(opd)+','+str(stopsperlineinmuni)+','+str(averagetpdperline)+','+str(mediantpdperline)+',|,'+','.join(map(str,tpdlist))+'\n'
		postsline = muni_id+','+line_name+','+str(opd)+','+str(stopsperlineinmuni)+','+str(averagetpdperline)+','+str(mediantpdperline)+'\n'
		fileout.write(postsline)
		
		munisforoutput_dict[muni_id][2][line_name] = [opd, stopsperlineinmuni, averagetpdperline, mediantpdperline] # collect tpdperline_dict in munisforoutput_dict
		total_muni_opd += opd
		total_muni_tpd += averagetpdperline
		
	munisforoutput_dict[muni_id][0] = total_muni_opd # collect in munisforoutput_dict
	munisforoutput_dict[muni_id][1] = total_muni_tpd # collect in munisforoutput_dict

# for each town 
for feature in town_geo['features']:
# get muni boarders multipoly to use as filter
	#print feature['properties']
	muni_id = feature['properties']['muni_id']
	muni_name = feature['properties']['muni_name']
	print muni_name
	muni_boarder_multipoly = shape(feature['geometry']) # get muni boarders multipoly to use as filter
	#print len(feature['geometry']['coordinates']), muni_boarder_multipoly.geom_type
	#print feature['geometry']['coordinates'][0][0][0]
	if not muni_boarder_multipoly.is_valid : 
		muni_boarder_multipoly = muni_boarder_multipoly.buffer(0) # clean multipoly if not valid
		print 'cleaned multipoly'

# filter stops w tpd per line in boarders multipoly 
	muni_tpdperline_dict = {} # line_name:[totalopd,[tpd1,tpd2,tpd3...]]
	stopinmunicount = 0
	opdinmuni = 0
	linesinmuni = 0
	for stop_id, [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict] in stops_dict.iteritems() :
		stop_loc = Point(stop_lon, stop_lat)
		if muni_boarder_multipoly.contains(stop_loc) :
			muni_stops_dict[stop_id] = muni_id
			#print stop_loc
			stopinmunicount +=1

# merge the tpd per line from stop in muni
			#print maxdaytpdperline_dict
			for line_name, tpd in maxdaytpdperline_dict.iteritems() :
				clean_line_name = ''
				for i in range(len(line_name)): # stupid workaround for unicode problem of aleph in route_short_name
					lnchar = line_name[i]
					if lnchar == '-' : lnchar = '-'
					elif lnchar > '9': lnchar = 'a'
					clean_line_name += lnchar
				line_name = clean_line_name
				#print line_name
				opdinmuni += tpd
				if line_name not in muni_tpdperline_dict : # not in merged dict then add it
					#muni_tpdperline_dict[line_name] = tpd # merge by sum
					muni_tpdperline_dict[line_name] = [tpd,[tpd]] # merge by sum and collecting
					linesinmuni +=1
				else: # already in merged dict then sum tpd
					#muni_tpdperline_dict[line_name] += tpd # merge by sum
					muni_tpdperline_dict[line_name][0] += tpd # merge by sum
					muni_tpdperline_dict[line_name][1].append(tpd) # and merge by collecting
	print 'stopinmunicount, linesinmuni, opdinmuni: ', stopinmunicount, linesinmuni, opdinmuni
	#print muni_tpdperline_dict

# output merged muni opportunities per day (opd) per line dict to txt file
#   and collect munisforoutput_dict for js output
	total_muni_opd = 0
	total_muni_tpd = 0
	tpdperline_dict = {}
	munisforoutput_dict[muni_id] = [total_muni_opd, total_muni_tpd, tpdperline_dict] # collect muni_id and placeholders
	#for line_name, [opd,tpdlist] in muni_tpdperline_dict.iteritems() :
	for line_name, [opd,tpdlist] in sorted(muni_tpdperline_dict.iteritems(), reverse=True, key=lambda(k,v): (v[0]/len(v[1]))):
		averagetpdperline = opd/len(tpdlist)
		stopsperlineinmuni = len(tpdlist)
		mediantpdperline = int(np.median(np.array(tpdlist)))
		#postsline = muni_id+','+line_name+','+str(opd)+','+str(stopsperlineinmuni)+','+str(averagetpdperline)+','+str(mediantpdperline)+',|,'+','.join(map(str,tpdlist))+'\n'
		postsline = muni_id+','+line_name+','+str(opd)+','+str(stopsperlineinmuni)+','+str(averagetpdperline)+','+str(mediantpdperline)+'\n'
		fileout.write(postsline)
		
		munisforoutput_dict[muni_id][2][line_name] = [opd, stopsperlineinmuni, averagetpdperline, mediantpdperline] # collect tpdperline_dict in munisforoutput_dict
		total_muni_opd += opd
		total_muni_tpd += averagetpdperline
		
	munisforoutput_dict[muni_id][0] = total_muni_opd # collect in munisforoutput_dict
	munisforoutput_dict[muni_id][1] = total_muni_tpd # collect in munisforoutput_dict

fileout.close()
print 'closed file: ', txtfileout

#
#   output js file with tpd per line (agency_id+route_short_name) in muni - 'muni_w_tpd_per_line'+'_'+servicedate+'.js
#
def getJSON(m_id):
	return {
		m_id: {
			"total_muni_opd": munisforoutput_dict[m_id][0],
			"total_muni_tpd": munisforoutput_dict[m_id][1],
			"tpdperline_dict": munisforoutput_dict[m_id][2] # no sort in py, sort in js during display
		}
	}

# saveGeoJSON

print ("Generating JSON export.")
json_list = [getJSON(muni_id) for muni_id in munisforoutput_dict]
print ("Saving file: " + gtfspathout+jsfileout+ " ...")
nf = open(gtfspathout+jsfileout, "w")
jsonstr = json.dumps(json_list, separators=(',',':')) # smaller file for download
outstr = jsonstr.replace('}},{', '},\n').replace('[{', '{').replace('}]', '}')
nf.write('var munisWtpdperline =\n')
nf.write(outstr)
nf.close()
print ("Saved file: " + jsfileout)

# output txt file of stop_id and muni_id the stop is in ('0' = not in Muni)
fileout = open(gtfspathout+stopstxtfileout, 'w') # open file to save results 
postsline = 'stop_id,muni_id\n'
fileout.write(postsline)
for stop_id, muni_id in muni_stops_dict.iteritems() :
	#print 'stop_id, muni_id : ', stop_id, muni_id
	postsline = stop_id+','+muni_id+'\n'
	fileout.write(postsline)
fileout.close()
print 'closed file: ', stopstxtfileout

print "Local current time :", time.asctime( time.localtime(time.time()) )