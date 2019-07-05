#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create a file with transit opportunities per day (opd) at munis 
# filter file with average tpd per stop and stop location, using muni boarder multipolygons in geojson files
# sum tpds at stops in muni to calculate opd for muni
#
# input:
#   gtfsdate = '20180425'
#   sserviceweekstartdate = '20180425'
#   pathin = 'C:\\transitanalyst\\processed\\'
#   pathout = 'C:\\transitanalyst\\processed\\'
#   txt file with average tpd per stop  - 'stopswtpdand10xforrail'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#   stopsinmuni_post_edit = 'stopsinmuni_post_edit'+'_'+servicedate+'.txt'
#   'muni_names.txt' - map names from muni_id to english to hebrew
# output:
#   txt file with average opd per muni  - 'muni_opd'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt'
#
#
print('----------------- create a file with transit opportunities per day (opd) at munis --------------------------')
print('sum tpds at stops in muni to calculate opd for muni')
print('generate muni_opd_[serviceweekstartdate]_[gtfsdate].txt')
from datetime import date
from datetime import timedelta
import time
import copy
import os
import json
import csv
from shapely.geometry import shape, Point, Polygon, MultiPolygon
import gtfs_config as gtfscfg
from pathlib import Path

cwd = Path.cwd()

def main(gtfsdate, processedpath, serviceweekstartdate):
	# input:
	sserviceweekstartdate = serviceweekstartdate
	pathin = cwd.parent / processedpath
	pathout = cwd.parent / processedpath
	stopsfilein = 'stopswtpdand10xforrail'+'_'+sserviceweekstartdate+'_'+gtfsdate+'.txt' # txt file with average tpd per stop and top location
	servicedate = sserviceweekstartdate
	stopsinmuni_post_edit = 'stopsinmuni_post_edit'+'_'+servicedate+'.txt'
	muninamesfilein = 'muni_names.txt'
	processedpathin = pathout
	parent_path = cwd.parent / processedpath

	# output:
	munifileout = stopsfilein.replace('stopswtpdand10xforrail', 'muni_opd') #  txt file with average opd per muni 
	print('stopsfilein, munifileout : ', stopsfilein, munifileout)

	gtfspathin = pathin
	gtfspathout = pathout

	#
	# load files 
	#

	#
	# scan stopfile to create munistops_dict and compute maxaveragetpdatstop and totaltripsatallstops
	#
	# 1st sline is 'stop_id,stop_lat,stop_lon,averagetpdatstop\n'
	#
	maxaveragetpdatstop = 0.0
	totaltripsatallstops = 0.0

	munistops_dict = {}
	slinelist=[]
	print(gtfspathin / stopsfilein)
	filein = open(gtfspathin / stopsfilein, 'r', encoding="utf8")
	sline = filein.readline()
	keylinelen = len(sline)
	slinelist=sline[:-1].split(",")
	print(slinelist)
	keylist = slinelist
	stop_id_i = keylist.index('stop_id')
	stop_lat_i = keylist.index('stop_lat')
	stop_lon_i = keylist.index('stop_lon')
	averagetpdatstop_i = keylist.index('averagetpdatstop')
	print(slinelist[stop_id_i], slinelist[stop_lat_i], slinelist[stop_lon_i], slinelist[averagetpdatstop_i])
	maxfilelinecount = gtfscfg.MAX_STOPS_COUNT
	count = 0
	sline = filein.readline()
	fileinlines = (os.path.getsize(gtfspathin / stopsfilein)-keylinelen)/len(sline)
	# scan stopsfilein
	while ((count < maxfilelinecount) and (sline != '')):
		slinelist=sline[:-1].split(",")
		#print (slinelist)
		stop_id = slinelist[stop_id_i]
		stop_lat = slinelist[stop_lat_i]
		stop_lon = slinelist[stop_lon_i]
		averagetpdatstop = float(slinelist[averagetpdatstop_i])
		maxaveragetpdatstop = max(maxaveragetpdatstop, averagetpdatstop)
		totaltripsatallstops += averagetpdatstop
		munistops_dict[stop_id] = [stop_lat, stop_lon, averagetpdatstop]
		count += 1
		#print count, fileinlines, averagetpdatstop, maxaveragetpdatstop, totaltripsatallstops
		sline = filein.readline()
	print('count, fileinlines, averagetpdatstop, maxaveragetpdatstop, totaltripsatallstops')
	print(count, fileinlines, averagetpdatstop, maxaveragetpdatstop, totaltripsatallstops)
	print('------------------')
	print('stops lines scanned ', count)
	filein.close()

	#
	# >>> load txt file of stopsinmuni post edit
	#
	print('>>> load txt file of stopsinmuni post edit')
	txtfilein = stopsinmuni_post_edit
	stopsinmuni = {}
	with open(processedpathin / txtfilein, newline='', encoding="utf8") as f:
		reader = csv.reader(f)
		header = next(reader) # ['muni_id', 'stop_id', 'part_in_muni']
		print(header)
		for row in reader:
			#print row
			muni_id = row[0]
			stop_id = row[1]
			part_in_muni = row[2]
			# add to dict
			if muni_id in stopsinmuni :
				stopsinmuni[muni_id][stop_id] = part_in_muni
			else :
				stopsinmuni[muni_id] = {}
				stopsinmuni[muni_id][stop_id] = part_in_muni
	print(stopsinmuni[muni_id]) # last one
	print('stopsinmuni loaded. muni count ', len(stopsinmuni))

	# >>> load muninames file
	muniid2engdict = {}
	with open(parent_path / muninamesfilein, newline='', encoding="utf8") as muninames_f:
		readermuninames = csv.reader(muninames_f)
		headermuninames = next(readermuninames) # muni_id,muni_name_h,muni_name_e
		print(headermuninames)
		for row in readermuninames:
			#print row
			muni_id = row[0]
			muni_name_h = row[1]
			muni_name_e = row[2]
			muniid2engdict[muni_id] = muni_name_e
	print(muniid2engdict[muni_id]) # print last one
	print('muniid2engdict loaded. muninames count ', len(muniid2engdict))

	#
	# process loaded files
	#

	#
	# for each muni 
	#   filter stops w tpd using stops in muni list 
	#   sum the tpd from all stops in muni to get opd for muni
	#   output muni opd to txt file
	#

	fileout = open(pathout / munifileout, 'w', encoding="utf8") # open file to save results 
	postsline = 'municode,muni_name,opdinmuni,stopinmunicount\n'
	fileout.write(postsline)

	# for each muni 
	for muni_id, stopsindict in stopsinmuni.items():
	# use stops in muni dict as filter
		muni_name = muniid2engdict[muni_id]
		print(muni_name)

	# filter stops w tpd using stops in muni list
		muni_stops_dict = {}
		stopinmunicount = 0.0
		opdinmuni = 0.0
		for stop_id, [stop_lat, stop_lon, averagetpdatstop] in munistops_dict.items() :
			if stop_id in stopsindict :
				part_in_muni = float(stopsindict[stop_id])
				stopinmunicount += part_in_muni
				opdinmuni += averagetpdatstop*part_in_muni # sum tpd per stop in muni to get opd
		print('stopinmunicount, opdinmuni: ', stopinmunicount, round(opdinmuni))
		#print muni_tpdperline_dict

	# output muni opportunities per day (opd) to txt file
		postsline = muni_id+','+muni_name+','+str(round(opdinmuni))+','+str(round(stopinmunicount))+'\n' 
		fileout.write(postsline)

	fileout.close()
	print('closed file: ', munifileout)


