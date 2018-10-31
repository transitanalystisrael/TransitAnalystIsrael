#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create geojson city and town boarders files with properties of muni_id, muni_name, built_area, population, muni_opd, muni_transitscore and fair-share_score
# boarders are multipolygons with holes in some of the polygons 
# for each city and town, need to collect all the basic information and then calculate the muni_transitscore and the fair-share_score
#
# muni-transitscore = 100*LOG10(transit-opportunities-persqkm-per15min)/LOG10(MAX (all transit-opportunities-persqkm-per15min))
# transit-opportunities-persqkm-per15min = 15*totaltripsinmuni /(built-area *12*16*60) 
#
# transit-above-or-below-fair-share = muni-transit-opportunities-perday / fair-share of muni-transit-opportunities-perday 
# fair-share of muni-transit-opportunities-perday = muni-population * total muni-transit-opportunities-perday / total population
#
# input:
#   gtfsdate = '20180425'
#   sserviceweekstartdate = '20180425'
#   pathin = 'C:\\transitanalyst\\processed\\'
#   pathout = 'C:\\transitanalyst\\processed\\'#   israel_city_boarders.geojson
#   israel_town_boarders.geojson # moatzot mekomiyot
#   muni_pop2016_built-area2013.csv
#   'muni_opd'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt' - txt file with average opd per muni  - muni_opd_20180425_20180425.txt
#
# output:
#   'israel_city_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
#   'israel_town_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
#   'muni_transitscore_xy.js' # file of muni_name: transitscore pairs
#   'muni_fairsharescore_xy.js' # file of muni_name: fairsharescore pairs
#   'muni_builtdensityscore_xy.js' # file of muni_name: builtdensityscore pairs
#

print '-----------------  create geojson city and town boarders files with properties of muni_id, muni_name, built_area, population, muni_tpd, muni_transitscore and fair-share_score --------------------------'
print ' output: israel_city_boarders_w_properties.geojson '
print ' output: israel_town_boarders_w_properties.geojson '

from datetime import date
from datetime import timedelta
import time
import math
import json
from shapely.geometry import shape, Point, Polygon
from shapely.validation import explain_validity
import csv
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#

SERVICE_DAYS_COUNT = 6 # usually count over two weeks or 12 service days, sometimes use one week or 6 service days
SERVICE15MININDAY = 4*16 # for compatability with transitscore in XLS

parent_path = 'C:\\transitanalyst\\processed\\'
pathin = parent_path
pathout = parent_path

# input:
gtfsdate = '20180425'
sserviceweekstartdate = '20180425'
cityfilein = 'israel_city_boarders.geojson'
townfilein = 'israel_town_boarders.geojson' # moatzot mekomiyot
muniinfofilein = 'muni_pop2016_built-area2013.csv'
munitransitfilein = 'muni_opd'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'

#output:
cityfileout = 'israel_city_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
townfileout = 'israel_town_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js' # moatzot mekomiyot
transitscorefileout = 'muni_transitscore_xy.js' # file of muni_name: transitscore pairs
fairsharescorefileout = 'muni_fairsharescore_xy.js' # file of muni_name: fairsharescore pairs
builtdensityscorefileout = 'muni_builtdensityscore_xy.js' # file of muni_name: builtdensityscore pairs

#
# load files 
#

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

# >>> load muniinfo file
muniinfodict = {}
with open(parent_path+muniinfofilein, 'rb') as muniinfo_f:
	readermuniinfo = csv.reader(muniinfo_f)
	headermuniinfo = readermuniinfo.next() # muni_code,pop,built-area
	print headermuniinfo
	for row in readermuniinfo:
		#print row
		muni_id = row[0]
		pop = row[1]
		built_area = row[2]
		muniinfodict[muni_id] = [pop, built_area]
print muniinfodict[muni_id] # print last one
print 'muniinfodict loaded. muniinfo count ', len(muniinfodict)

# >>> load munitransit file
munitransitdict = {}

with open(parent_path+munitransitfilein, 'rb') as munitransit_f:
	readermunitransit = csv.reader(munitransit_f)
	headermunitransit = readermunitransit.next() # municode,muni_name,muniopd,stopsinmuni
	print headermunitransit
	for row in readermunitransit:
		#print row
		muni_id = row[0]
		muni_name = row[1]
		muni_opd = row[2]
		muni_stopscount = row[3]
		munitransitdict[muni_id] = [muni_opd, muni_stopscount]
print munitransitdict[muni_id] # print last one
print 'munitransitdict loaded. munitransit count ', len(munitransitdict)

#
# process loaded files
#
# 1st pass of 2
#
# add properties to features in city_geo 
# scan all features and use muni_id to look up additional properties
# compute and add muni_opdpsqkm and find max of muni_opdpsqkm
# compute total_muni_opd and total_muni_pop
max_muni_opdpsqkm = 0
total_muni_opd = 0
total_muni_pop = 0
for feature in city_geo['features']:
	#print feature['geometry']
	#print feature['properties']
	muni_id = feature['properties']['muni_id']
	#feature['properties']['muni_type'] = 'city'
	spopulation = muniinfodict[muni_id][0]
	sbuilt_area = muniinfodict[muni_id][1]
	smuni_opd = munitransitdict[muni_id][0]
	feature['properties']['pop'] = spopulation
	feature['properties']['built_area'] = sbuilt_area
	feature['properties']['muni_opd'] = smuni_opd
	population = int(spopulation)
	built_area = float(sbuilt_area)
	muni_opd = int(smuni_opd)
	muni_opdpsqkm = muni_opd / built_area
	feature['properties']['muni_opdpsqkm'] = str(round(muni_opdpsqkm,2))
	max_muni_opdpsqkm = max(max_muni_opdpsqkm, muni_opdpsqkm)
	total_muni_opd += muni_opd
	total_muni_pop += population
	print feature['properties']
print 'max_muni_opdpsqkm: ', max_muni_opdpsqkm
print 'total_muni_opd: ', total_muni_opd
print 'total_muni_pop: ', total_muni_pop

# add properties to features in town_geo 
# scan all features and use muni_id to look up additional properties
# compute and add muni_opdpsqkm and find max of muni_opdpsqkm
# compute total_muni_opd and total_muni_pop
for feature in town_geo['features']:
	#print feature['geometry']
	#print feature['properties']
	muni_id = feature['properties']['muni_id']
	#feature['properties']['muni_type'] = 'city'
	spopulation = muniinfodict[muni_id][0]
	sbuilt_area = muniinfodict[muni_id][1]
	smuni_opd = munitransitdict[muni_id][0]
	feature['properties']['pop'] = spopulation
	feature['properties']['built_area'] = sbuilt_area
	feature['properties']['muni_opd'] = smuni_opd
	population = int(spopulation)
	built_area = float(sbuilt_area)
	muni_opd = int(smuni_opd)
	muni_opdpsqkm = muni_opd / built_area
	feature['properties']['muni_opdpsqkm'] = str(round(muni_opdpsqkm,2))
	max_muni_opdpsqkm = max(max_muni_opdpsqkm, muni_opdpsqkm)
	total_muni_opd += muni_opd
	total_muni_pop += population
	print feature['properties']
print 'max_muni_opdpsqkm: ', max_muni_opdpsqkm
print 'total_muni_opd: ', total_muni_opd
print 'total_muni_pop: ', total_muni_pop

# 2nd pass of 2
#
# add properties to features in city_geo 
# scan all features 
# compute and add muni_transitscore
# compute and add muni_fairsharescore
for feature in city_geo['features']:
	#print feature['geometry']
	#print feature['properties']
	#print feature['properties']['muni_id']
	# compute and add muni_transitscore
	muni_opdpsqkm = float(feature['properties']['muni_opdpsqkm'])
	muni_transitscore = 100*math.log10(muni_opdpsqkm/SERVICE15MININDAY+1.0)/math.log10(max_muni_opdpsqkm/SERVICE15MININDAY+1.0)
	feature['properties']['transitscore'] = str(round(muni_transitscore,2))
	# compute and add muni_fairsharescore
	muni_opd = float(feature['properties']['muni_opd'])
	population = float(feature['properties']['pop'])
	muni_fairsharescore = 100 * muni_opd / (population * total_muni_opd / total_muni_pop)
	feature['properties']['fairsharescore'] = str(round(muni_fairsharescore,2))
	#print feature['properties']

print feature # last one

# add properties to features in town_geo 
# scan all features 
# compute and add muni_transitscore
# compute and add muni_fairsharescore
for feature in town_geo['features']:
	#print feature['geometry']
	#print feature['properties']
	#print feature['properties']['muni_id']
	# compute and add muni_transitscore
	muni_opd = float(feature['properties']['muni_opd'])
	muni_opdpsqkm = float(feature['properties']['muni_opdpsqkm'])
	muni_transitscore = 100*math.log10(muni_opdpsqkm/SERVICE15MININDAY+1.0)/math.log10(max_muni_opdpsqkm/SERVICE15MININDAY+1.0)
	feature['properties']['transitscore'] = str(round(muni_transitscore,2))
	# compute and add muni_fairsharescore
	population = float(feature['properties']['pop'])
	muni_fairsharescore = 100 * muni_opd / (population * total_muni_opd / total_muni_pop)
	feature['properties']['fairsharescore'] = str(round(muni_fairsharescore,2))
	#print feature['properties']

print feature # last one

#
# output processed data to files
#
# saveGeoJSON
print ("Generating GeoJSON export.")

geojson_file_name = cityfileout
print ("Saving file: " + pathout+geojson_file_name + " ...")
nf = open(pathout+geojson_file_name, "w")
#json.dump(city_geo, nf, indent=4)
jsonstr = json.dumps(city_geo, separators=(',',':')) # smaller file for download
outstr = jsonstr.replace('}},', '}},\n')
nf.write('var cityBoarders =\n')
nf.write(outstr)
nf.close()
print ("Saved file: " + geojson_file_name)

geojson_file_name = townfileout
print ("Saving file: " + pathout+geojson_file_name + " ...")
nf = open(pathout+geojson_file_name, "w")
#json.dump(town_geo, nf, indent=4)
jsonstr = json.dumps(town_geo, separators=(',',':')) # smaller file for download
outstr = jsonstr.replace('}},', '}},\n')
nf.write('var townBoarders =\n')
nf.write(outstr)
nf.close()
print ("Saved file: " + geojson_file_name)

# create transitscore and fairsharescore and builtdensityscore dicts for output
transitscoredict = {}
fairsharescoredict = {}
builtdensityscoredict ={}
for feature in city_geo['features']:
	transitscoredict[feature['properties']['muni_name']] = float(feature['properties']['transitscore'])
	fairsharescoredict[feature['properties']['muni_name']] = float(feature['properties']['fairsharescore'])
	builtdensityscoredict[feature['properties']['muni_name']] = round(float(feature['properties']['pop'])/float(feature['properties']['built_area']))
for feature in town_geo['features']:
	transitscoredict[feature['properties']['muni_name']] = float(feature['properties']['transitscore'])
	fairsharescoredict[feature['properties']['muni_name']] = float(feature['properties']['fairsharescore'])
	builtdensityscoredict[feature['properties']['muni_name']] = round(float(feature['properties']['pop'])/float(feature['properties']['built_area']))

# sort dicts for output
tslist = sorted(transitscoredict.iteritems(), key=lambda (k,v): (v,k), reverse=True)
fsslist = sorted(fairsharescoredict.iteritems(), key=lambda (k,v): (v,k), reverse=True)
bdslist = sorted(builtdensityscoredict.iteritems(), key=lambda (k,v): (v,k), reverse=True)
#print tslist
#print fsslist

# save chart xy files
xy_file_name1 = transitscorefileout
print ("Saving file: " + pathout+xy_file_name1 + " ...")
nf1 = open(pathout+xy_file_name1, "w")
outstr1 = 'var chartxy = {\n'

xy_file_name2 = fairsharescorefileout
print ("Saving file: " + pathout+xy_file_name2 + " ...")
nf2 = open(pathout+xy_file_name2, "w")
outstr2 = 'var chartxy = {\n'

xy_file_name3 = builtdensityscorefileout
print ("Saving file: " + pathout+xy_file_name3 + " ...")
nf3 = open(pathout+xy_file_name3, "w")
outstr3 = 'var chartxy = {\n'

'''
for feature in city_geo['features']:
	nf1.write(outstr1)
	outstr1 = '"' + feature['properties']['muni_name'] + '": ' + feature['properties']['transitscore']+',\n'

	nf2.write(outstr2)
	outstr2 = '"' + feature['properties']['muni_name'] + '": ' + feature['properties']['fairsharescore']+',\n'


for feature in town_geo['features']:
	nf1.write(outstr1)
	outstr1 = '"' + feature['properties']['muni_name'] + '": ' + feature['properties']['transitscore']+',\n'

	nf2.write(outstr2)
	outstr2 = '"' + feature['properties']['muni_name'] + '": ' + feature['properties']['fairsharescore']+',\n'
'''

for (muni_name1, ts) in tslist :
	nf1.write(outstr1)
	outstr1 = '"'+ muni_name1 + '": ' + str(ts)+',\n'
	
for (muni_name2, fss) in fsslist :
	nf2.write(outstr2)
	outstr2 = '"'+ muni_name2 + '": ' + str(fss)+',\n'
	
for (muni_name3, bds) in bdslist :
	nf3.write(outstr3)
	outstr3 = '"'+ muni_name3 + '": ' + str(bds)+',\n'

nf1.write(outstr1[:-2]+'\n')
nf1.write('};')
nf1.close()
print ("Saved file: " + xy_file_name1)

nf2.write(outstr2[:-2]+'\n')
nf2.write('};')
nf2.close()
print ("Saved file: " + xy_file_name2)

nf3.write(outstr3[:-2]+'\n')
nf3.write('};')
nf3.close()
print ("Saved file: " + xy_file_name3)