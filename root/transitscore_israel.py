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
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
processdate = process_date.get_date_now()

GTFS_transitscore_for_all_israel_7.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath) # takes two hours so do some tests without it, but remember to put it back!!!
transitscore_txt2jsobject_v1.main(processdate, cfg.gtfsdirbase, cfg.processedpath)
transitscore_array2raster_v3.main(processdate, cfg.gtfsdirbase, cfg.processedpath)

print("Local current time :", time.asctime( time.localtime(time.time()) ))