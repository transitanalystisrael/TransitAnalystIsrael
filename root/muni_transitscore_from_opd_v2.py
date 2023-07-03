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
#   muni_pop2017_built-area2017.csv (changed to 2022)
#   'muni_opd'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt' - txt file with average opd per muni  - muni_opd_20180425_20180425.txt
#   'muni_names.txt' - map names from english to hebrew
#
# output:
#   'israel_city_boarders.js' 
#   'israel_town_boarders.js'
#   'israel_city_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
#   'israel_town_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
#   'muni_transitscore_xy.js' # file of muni_name: transitscore pairs
#   'muni_fairsharescore_xy.js' # file of muni_name: fairsharescore pairs
#   'muni_builtdensityscore_xy.js' # file of muni_name: builtdensityscore pairs
#

print('-----------------  create geojson city and town boarders files with properties of muni_id, muni_name, built_area, population, muni_tpd, muni_transitscore and fair-share_score --------------------------')
print(' output: israel_city_boarders_w_properties.geojson ')
print(' output: israel_town_boarders_w_properties.geojson ')

from datetime import date
from datetime import timedelta
import time
import math
import json
from shapely.geometry import shape, Point, Polygon
from shapely.validation import explain_validity
import csv
from pathlib import Path

cwd = Path.cwd()
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
def main(gtfsdate, processedpath, serviceweekstartdate, language):
	SERVICE_DAYS_COUNT = 6 # use one week or 6 service days
	SERVICE15MININDAY = 4*16 # for compatability with transitscore in XLS

	parent_path = cwd.parent / processedpath
	pathin = parent_path
	pathout = parent_path

	# input:
	sserviceweekstartdate = serviceweekstartdate
	cityfilein = 'israel_city_boarders.geojson'
	townfilein = 'israel_town_boarders.geojson' # moatzot mekomiyot
	#muniinfofilein = 'muni_pop2017_built-area2017.csv'
	muniinfofilein = 'muni_pop2022_built-area2022.csv'
	munitransitfilein = 'muni_opd'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
	muninamesfilein = 'muni_names.txt'

	#output:
	cityfileout1 = 'israel_city_boarders.js'
	townfileout1 = 'israel_town_boarders.js'
	cityfileout = 'israel_city_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js'
	townfileout = 'israel_town_boarders_w_properties'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.js' # moatzot mekomiyot
	transitscorefileout = 'muni_transitscore_xy.js' # file of muni_name: transitscore pairs
	fairsharescorefileout = 'muni_fairsharescore_xy.js' # file of muni_name: fairsharescore pairs
	builtdensityscorefileout = 'muni_builtdensityscore_xy.js' # file of muni_name: builtdensityscore pairs

	#
	# load files 
	#

	# >>> load city boarders 
	with open(parent_path / cityfilein) as cf:
		city_geo = json.load(cf)
	print('loaded city geo, feature count: ', len(city_geo['features']))
	#print city_geo

	# >>> load town boarders 
	with open(parent_path / townfilein) as tf:
		town_geo = json.load(tf)
	print('loaded town geo, feature count: ', len(town_geo['features']))
	#print town_geo

	# >>> load muniinfo file
	muniinfodict = {}
	with open(parent_path / muniinfofilein, newline='', encoding="utf8") as muniinfo_f:
		readermuniinfo = csv.reader(muniinfo_f)
		headermuniinfo = next(readermuniinfo) # muni_code,pop,built-area
		print(headermuniinfo)
		for row in readermuniinfo:
			#print row
			muni_id = row[0]
			pop = row[1]
			built_area = row[2]
			muniinfodict[muni_id] = [pop, built_area]
	print(muniinfodict[muni_id]) # print last one
	print('muniinfodict loaded. muniinfo count ', len(muniinfodict))

	# >>> load munitransit file
	munitransitdict = {}
	with open(parent_path / munitransitfilein, newline='', encoding="utf8") as munitransit_f:
		readermunitransit = csv.reader(munitransit_f)
		headermunitransit = next(readermunitransit) # municode,muni_name,muniopd,stopsinmuni
		print(headermunitransit)
		for row in readermunitransit:
			#print row
			muni_id = row[0]
			muni_name = row[1]
			muni_opd = row[2]
			muni_stopscount = row[3]
			munitransitdict[muni_id] = [muni_opd, muni_stopscount]
	print(munitransitdict[muni_id]) # print last one
	print('munitransitdict loaded. munitransit count ', len(munitransitdict))

	# >>> load muninames file
	muninameseng2hebdict = {}
	with open(parent_path / muninamesfilein, newline='', encoding="utf8") as muninames_f:
		readermuninames = csv.reader(muninames_f)
		headermuninames = next(readermuninames) # muni_id,muni_name_h,muni_name_e
		print(headermuninames)
		for row in readermuninames:
			#print row
			muni_id = row[0]
			muni_name_h = row[1]
			muni_name_e = row[2]
			muninameseng2hebdict[muni_name_e] = muni_name_h
	print(muninameseng2hebdict[muni_name_e]) # print last one
	print('muninameseng2hebdict loaded. muninames count ', len(muninameseng2hebdict))

	#
	# process loaded files
	#
	
	# add muni_name in hebrew and output js file before adding other properties
	
	for feature in city_geo['features']:
		muni_name_e = feature['properties']['muni_name']
		feature['properties']['muni_name_h'] = muninameseng2hebdict[muni_name_e]
	for feature in town_geo['features']:
		muni_name_e = feature['properties']['muni_name']
		feature['properties']['muni_name_h'] = muninameseng2hebdict[muni_name_e]
	
	geojson_file_name = cityfileout1
	print(("Saving file: ", pathout / geojson_file_name ,  " ..."))
	nf = open(pathout / geojson_file_name, "w", encoding="utf8")
	#json.dump(city_geo, nf, indent=4)
	jsonstr = json.dumps(city_geo, separators=(',',':')) # smaller file for download
	outstr = jsonstr.replace('}},', '}},\n')
	nf.write('var cityBoarders =\n')
	nf.write(outstr)
	nf.close()
	print(("Saved file: " + geojson_file_name))

	geojson_file_name = townfileout1
	print(("Saving file: ", pathout / geojson_file_name ,  " ..."))
	nf = open(pathout / geojson_file_name, "w", encoding="utf8")
	#json.dump(town_geo, nf, indent=4)
	jsonstr = json.dumps(town_geo, separators=(',',':')) # smaller file for download
	outstr = jsonstr.replace('}},', '}},\n')
	nf.write('var townBoarders =\n')
	nf.write(outstr)
	nf.close()
	print(("Saved file: " + geojson_file_name))

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
		if muni_id in munitransitdict :
			smuni_opd = munitransitdict[muni_id][0]
		else:
			smuni_opd = '0'
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
		#print feature['properties']
	print('max_muni_opdpsqkm: ', max_muni_opdpsqkm)
	print('total_muni_opd: ', total_muni_opd)
	print('total_muni_pop: ', total_muni_pop)

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
		if muni_id in munitransitdict :
			smuni_opd = munitransitdict[muni_id][0]
		else:
			smuni_opd = '0'
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
		print(feature['properties'])
	print('max_muni_opdpsqkm: ', max_muni_opdpsqkm)
	print('total_muni_opd: ', total_muni_opd)
	print('total_muni_pop: ', total_muni_pop)

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

	print(feature) # last one

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

	print(feature) # last one

	#
	# output processed data to files
	#
	# saveGeoJSON
	print ("Generating GeoJSON export.")

	geojson_file_name = cityfileout
	print(("Saving file: ", pathout / geojson_file_name ,  " ..."))
	nf = open(pathout / geojson_file_name, "w", encoding="utf8")
	#json.dump(city_geo, nf, indent=4)
	jsonstr = json.dumps(city_geo, separators=(',',':')) # smaller file for download
	outstr = jsonstr.replace('}},', '}},\n')
	nf.write('var cityBoarders =\n')
	nf.write(outstr)
	nf.close()
	print(("Saved file: " + geojson_file_name))

	geojson_file_name = townfileout
	print(("Saving file: ", pathout / geojson_file_name ,  " ..."))
	nf = open(pathout / geojson_file_name, "w", encoding="utf8")
	#json.dump(town_geo, nf, indent=4)
	jsonstr = json.dumps(town_geo, separators=(',',':')) # smaller file for download
	outstr = jsonstr.replace('}},', '}},\n')
	nf.write('var townBoarders =\n')
	nf.write(outstr)
	nf.close()
	print(("Saved file: " + geojson_file_name))

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
	tslist = sorted(iter(transitscoredict.items()), key=lambda k_v: (k_v[1],k_v[0]), reverse=True)
	fsslist = sorted(iter(fairsharescoredict.items()), key=lambda k_v1: (k_v1[1],k_v1[0]), reverse=True)
	bdslist = sorted(iter(builtdensityscoredict.items()), key=lambda k_v2: (k_v2[1],k_v2[0]), reverse=True)
	#print tslist
	#print fsslist

	# save chart xy files
	xy_file_name1 = transitscorefileout
	print(("Saving file: ", pathout / xy_file_name1 ,  " ..."))
	nf1 = open(pathout / xy_file_name1, "w", encoding="utf8")
	outstr1 = 'var chartxy = {\n'

	xy_file_name2 = fairsharescorefileout
	print(("Saving file: ", pathout / xy_file_name2 ,  " ..."))
	nf2 = open(pathout / xy_file_name2, "w", encoding="utf8")
	outstr2 = 'var chartxy = {\n'

	xy_file_name3 = builtdensityscorefileout
	print(("Saving file: ", pathout / xy_file_name3 ,  " ..."))
	nf3 = open(pathout / xy_file_name3, "w", encoding="utf8")
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
	#print muninameseng2hebdict
	for (muni_name1, ts) in tslist :
		nf1.write(outstr1)
		if language == 'hebrew' : 
			#print muni_name1
			muni_name = muninameseng2hebdict[muni_name1]
		else :
			muni_name = muni_name1
		outstr1 = '"'+ muni_name + '": ' + str(ts)+',\n'
		
	for (muni_name2, fss) in fsslist :
		nf2.write(outstr2)
		if language == 'hebrew' : 
			muni_name = muninameseng2hebdict[muni_name2]
		else :
			muni_name = muni_name2
		outstr2 = '"'+ muni_name + '": ' + str(fss)+',\n'
		
	for (muni_name3, bds) in bdslist :
		nf3.write(outstr3)
		if language == 'hebrew' : 
			muni_name = muninameseng2hebdict[muni_name3]
		else :
			muni_name = muni_name3
		outstr3 = '"'+ muni_name + '": ' + str(bds)+',\n'

	nf1.write(outstr1[:-2]+'\n')
	nf1.write('};')
	nf1.close()
	print(("Saved file: " + xy_file_name1))

	nf2.write(outstr2[:-2]+'\n')
	nf2.write('};')
	nf2.close()
	print(("Saved file: " + xy_file_name2))

	nf3.write(outstr3[:-2]+'\n')
	nf3.write('};')
	nf3.close()
	print(("Saved file: " + xy_file_name3))
	