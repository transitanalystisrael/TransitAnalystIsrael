#!/usr/bin/env python
#--------------------------------------------------
# Geo filter GTFS for all of Israel based on given polygon - typically of a city
# input GTFS dir israelyyyymmdd is expected in transitanalyst\\gtfs directory and as a command line argument 
# output GTFS dir israelyyyymmdd_israel-cityname will be created in transitanalyst\\processed
# need to set cityname and geofilter polygon below
#------------------------------------------------------------------------------------------
#----------------------------------------------------
# filter the GTFS files by a given area polygon, keep only trips that both start and end in city
#--------------------------------------------------
import GTFS_geo_filter_startendstop
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
cityname = 'mahoz_tel_aviv'
geo_filter = [(32.145712,34.7900311),(32.0945361,34.7536389),(31.9868569,34.7241131),(31.9507415,34.7817913),(31.9460804,34.8120037),(31.9332612,34.815437),(31.921023,34.8360363),(31.9146119,34.8635022),(31.9198574,34.8827282),(31.9443324,34.8985211),(31.9507415,34.9101941),(31.9629757,34.9033276),(31.9763732,34.9040142),(31.9606455,34.9383465),(31.9763732,34.9905316),(32.0299438,34.999458),(32.1032613,34.9850384),(32.102098,34.9754254),(32.1108224,34.9500195),(32.1224538,34.8930279),(32.1154751,34.879295),(32.1381537,34.8223034),(32.1381537,34.8126904),(32.145712,34.7900311)
    ]
#*************************************************************************
gtfs_area_dir = gtfsdir+'_israel-'+cityname
gtfspathout = parent_path+'processed\\'+gtfs_area_dir+'\\'
if not os.access('processed\\'+gtfs_area_dir, os.F_OK): os.mkdir('processed\\'+gtfs_area_dir)
GTFS_geo_filter_startendstop.main(gtfspathin, gtfspathout, geo_filter)
print 'gtfspathin, gtfspathout, geo_filter : ', gtfspathin, gtfspathout, geo_filter
print 'filter done for ', cityname