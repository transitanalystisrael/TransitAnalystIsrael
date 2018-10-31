#!/usr/bin/env python
#--------------------------------------------------
# Geo filter GTFS for all of Israel based on given polygon - typically of a city
# input GTFS dir israelyyyymmdd is expected in transitanalyst\\gtfs directory and as a command line argument 
# output GTFS dir israelyyyymmdd_israel-cityname will be created in transitanalyst\\processed
# need to set cityname and geofilter polygon below
#------------------------------------------------------------------------------------------
#----------------------------------------------------
# filter the GTFS files by a given area polygon
#--------------------------------------------------
import GTFS_geo_filter_full
import os
import sys
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
# to enter inputs: change city name and geo_filter city polygon below
#***********************************************************************
cityname = 'arad'
geo_filter = [
    (31.2845659,35.1155663),(31.1866651,35.1159096),(31.1871202,35.1695418),(31.2318852,35.2250862),(31.2602772,35.2565031),(31.292194,35.229721)
    ]
#*************************************************************************
gtfs_area_dir = gtfsdir+'_israel-'+cityname
gtfspathout = parent_path+'processed\\'+gtfs_area_dir+'\\'
if not os.access('processed\\'+gtfs_area_dir, os.F_OK): os.mkdir('processed\\'+gtfs_area_dir)
GTFS_geo_filter_full.main(gtfspathin, gtfspathout, geo_filter)
print 'gtfspathin, gtfspathout, geo_filter : ', gtfspathin, gtfspathout, geo_filter
print 'filter done for ', cityname