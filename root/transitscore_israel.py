#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# calculate transitscore for every 100m x 100m square in israel.
# output raster heatmap for display on map and 
# output lookup table of results for score display popup on click on map
#

import transitanalystisrael_config as cfg
import process_date
import GTFS_transitscore_for_all_israel_7
import transitscore_txt2jsobject_v1
import transitscore_array2raster_v3
import time
import os

# change GDAL_DATA environment variable
gdal_data_dir_before = os.getenv('GDAL_DATA')
print(gdal_data_dir_before)
os.environ['GDAL_DATA'] = 'C:\Program Files\GDAL\gdal-data'
gdal_data_dir_after = os.getenv('GDAL_DATA')
print(gdal_data_dir_after)

#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
processdate = process_date.get_date_now()

GTFS_transitscore_for_all_israel_7.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath) # takes two hours so do some tests without it, but remember to put it back!!!
transitscore_txt2jsobject_v1.main(processdate, cfg.gtfsdirbase, cfg.processedpath)
transitscore_array2raster_v3.main(processdate, cfg.gtfsdirbase, cfg.processedpath)

# change back GDAL_DATA environment variable
os.environ['GDAL_DATA'] = gdal_data_dir_before
gdal_data_dir = os.getenv('GDAL_DATA')
print(gdal_data_dir)

print("Local current time :", time.asctime( time.localtime(time.time()) ))