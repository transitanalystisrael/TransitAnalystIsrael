#!/usr/bin/env python
# Split the Israel GTFS files into 4 GTFS files for 4 overlapping areas: Tel-Aviv Metro, Jerusalem, North, South
# input arg is path to uncompressed Israel GTFS dir
# outputs are GTFS directories for North, South, Tel-Aviv Metro and Jerusalem, created in the parent directory of the input dir
# also creat a small GTFS dir for use in testing using the region of Ramat-Aviv_Gimel
#
print "GTFS Israel Geo Split"
import os
import sys
import argparse
import GTFS_geo_filter_full

parser = argparse.ArgumentParser()
parser.add_argument("GTFS_dir_path", help="path to uncompressed Israel GTFS dir")
args = parser.parse_args()
print args.GTFS_dir_path
in_path = args.GTFS_dir_path
if in_path[-1]=='\\': in_path=in_path[:-1]
print os.getcwd()
#print in_path.rfind('\\')
gtfs_dir = in_path[in_path.rfind('\\')+1:]
gtfs_date = gtfs_dir[-8:]
parent_path = in_path[:in_path.rfind('\\')]
grand_parent_path = parent_path[:parent_path.rfind('\\')]
out_folder = 'processed'
os.chdir(grand_parent_path+'\\'+out_folder) # Changing the directory
print os.getcwd()
#print 'in_path,gtfs_dir,gtfs_date,parent_path,grand_parent_path : ',in_path,gtfs_dir,gtfs_date,parent_path,grand_parent_path
#print os.listdir(os.getcwd())
#------
gtfs_area_dir = 'israel_telavivmetro'+gtfs_date
if not os.access(gtfs_area_dir, os.F_OK): os.mkdir(gtfs_area_dir)
gtfspathin = in_path+'\\'
gtfspathout = grand_parent_path+'\\'+out_folder+'\\'+gtfs_area_dir+'\\'
#
geo_filter = [(32.525974,34.376221),
              (32.528289,35.071106),
              (31.629998,35.071106),
              (31.763202,34.411926)]
#
GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
print '---- saved filtered files in ', gtfspathout
#
#------
gtfs_area_dir = 'israel_jerusalem'+gtfs_date
if not os.access(gtfs_area_dir, os.F_OK): os.mkdir(gtfs_area_dir)
gtfspathin = in_path+'\\'
gtfspathout = grand_parent_path+'\\'+out_folder+'\\'+gtfs_area_dir+'\\'
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
print '---- saved filtered files in ', gtfspathout
#
#------
gtfs_area_dir = 'israel_north'+gtfs_date
if not os.access(gtfs_area_dir, os.F_OK): os.mkdir(gtfs_area_dir)
gtfspathin = in_path+'\\'
gtfspathout = grand_parent_path+'\\'+out_folder+'\\'+gtfs_area_dir+'\\'
#
geo_filter = [
    (33.363512395936034,34.716906738281295),
    (33.370393945357044,36.038012695312545),
    (32.24387927518177,36.073718261718795),
    (32.41098238817009,34.758105468750045)]
#
GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
print '---- saved filtered files in ', gtfspathout
#
#------
gtfs_area_dir = 'israel_south'+gtfs_date
if not os.access(gtfs_area_dir, os.F_OK): os.mkdir(gtfs_area_dir)
gtfspathin = in_path+'\\'
gtfspathout = grand_parent_path+'\\'+out_folder+'\\'+gtfs_area_dir+'\\'
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
print '---- saved filtered files in ', gtfspathout
#
#------
gtfs_area_dir = 'israel_ramatavivgimel'+gtfs_date
if not os.access(gtfs_area_dir, os.F_OK): os.mkdir(gtfs_area_dir)
gtfspathin = in_path+'\\'
gtfspathout = grand_parent_path+'\\'+out_folder+'\\'+gtfs_area_dir+'\\'
#
geo_filter = [
    (32.13437749119699, 34.78600044250493),
    (32.12798127926025, 34.81260795593266),
    (32.1179499530071, 34.812264633178756),
    (32.12383803904156, 34.7817089080811)]
#
GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
print '---- saved filtered files in ', gtfspathout
#
#
#print os.listdir(os.getcwd())
print '----------- Israel GTFS files have been split into 4 GTFS files for 4 overlapping areas: Tel-Aviv Metro, Jerusalem, North, South'


