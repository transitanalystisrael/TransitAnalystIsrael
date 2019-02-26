#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Split the Israel GTFS files into 4 GTFS files for 4 overlapping areas: Tel-Aviv Metro, Jerusalem, North, South
# input param is path to uncompressed Israel GTFS dir
# outputs are GTFS directories for North, South, Tel-Aviv Metro and Jerusalem, created in the output path
# also creat a small GTFS dir for use in testing using the region of Ramat-Aviv_Gimel
#
print("GTFS Israel Geo Split importing")
import os
import GTFS_geo_filter_full

def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
	#------
	gtfs_area_dir = gtfsdirbase+'_telavivmetro'+gtfsdate
	if not os.access(pathout+gtfs_area_dir, os.F_OK): os.mkdir(pathout+gtfs_area_dir)
	gtfspathin = gtfsparentpath+gtfsdirbase+gtfsdate+'\\'
	gtfspathout = pathout+gtfs_area_dir+'\\'
	#
	geo_filter = [(32.525974,34.376221),
				  (32.528289,35.071106),
				  (31.629998,35.071106),
				  (31.763202,34.411926)]
	#
	GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
	print('---- saved filtered files in ', gtfspathout)
	#
	#------
	gtfs_area_dir = gtfsdirbase+'_jerusalem'+gtfsdate
	if not os.access(pathout+gtfs_area_dir, os.F_OK): os.mkdir(pathout+gtfs_area_dir)
	gtfspathin = gtfsparentpath+gtfsdirbase+gtfsdate+'\\'
	gtfspathout = pathout+gtfs_area_dir+'\\'
	#
	geo_filter = [
		(31.972845178914596,34.97577209472661),
		(31.979834682386635,35.37265319824223),
		(31.518559358863257,35.36304016113286),
		(31.523242003861338,34.82059020996098),
		(31.874936270620093,34.88650817871098),
		(31.96469008546811,34.97027893066411)]
	#
	GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
	print('---- saved filtered files in ', gtfspathout)
	#
	#------
	gtfs_area_dir = gtfsdirbase+'_north'+gtfsdate
	if not os.access(pathout+gtfs_area_dir, os.F_OK): os.mkdir(pathout+gtfs_area_dir)
	gtfspathin = gtfsparentpath+gtfsdirbase+gtfsdate+'\\'
	gtfspathout = pathout+gtfs_area_dir+'\\'
	#
	geo_filter = [
		(33.363512395936034,34.716906738281295),
		(33.370393945357044,36.038012695312545),
		(32.24387927518177,36.073718261718795),
		(32.41098238817009,34.758105468750045)]
	#
	GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
	print('---- saved filtered files in ', gtfspathout)
	#
	#------
	gtfs_area_dir = gtfsdirbase+'_south'+gtfsdate
	if not os.access(pathout+gtfs_area_dir, os.F_OK): os.mkdir(pathout+gtfs_area_dir)
	gtfspathin = gtfsparentpath+gtfsdirbase+gtfsdate+'\\'
	gtfspathout = pathout+gtfs_area_dir+'\\'
	#
	geo_filter = [
		(31.89475958053676, 34.596057128906295),
		(31.780425469725238, 34.914660644531295),
		(31.66594983010228, 34.953112792968795),
		(31.499826432047055, 35.620532226562545),
		(29.093079677663443, 34.931140136718795),
		(31.450634641645625, 33.945117187500045)]
	#
	GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
	print('---- saved filtered files in ', gtfspathout)
	#
	#------
	gtfs_area_dir = gtfsdirbase+'_ramatavivgimel'+gtfsdate
	if not os.access(pathout+gtfs_area_dir, os.F_OK): os.mkdir(pathout+gtfs_area_dir)
	gtfspathin = gtfsparentpath+gtfsdirbase+gtfsdate+'\\'
	gtfspathout = pathout+gtfs_area_dir+'\\'
	#
	geo_filter = [
		(32.13437749119699, 34.78600044250493),
		(32.12798127926025, 34.81260795593266),
		(32.1179499530071, 34.812264633178756),
		(32.12383803904156, 34.7817089080811)]
	#
	GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
	print('---- saved filtered files in ', gtfspathout)
	#
	#
	#print os.listdir(os.getcwd())
	print('----------- Israel GTFS files have been split into 4 GTFS files for 4 overlapping areas: Tel-Aviv Metro, Jerusalem, North, South')

