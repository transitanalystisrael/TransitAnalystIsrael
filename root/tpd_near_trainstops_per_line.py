#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# collect a set of trip_id s at all stops in a GTFS file over the selected week of the service period starting at serviceweekstartdate
# filter stops near trainstations based on input txt file - stopsneartrainstop_post_edit
# merge sets of trips at stops near each trainstation to count trips per hour and per day
#
#

import transitanalystisrael_config as cfg
import process_date
import trip_ids_at_stops_merge_near_trainstops_perday_v3
import stopswtrainstopidsandtpdperline_v1
import time
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
processdate = process_date.get_date_now()

trip_ids_at_stops_merge_near_trainstops_perday_v3.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, processdate)
stopswtrainstopidsandtpdperline_v1.main(processdate, cfg.processedpath)

print("Local current time :", time.asctime( time.localtime(time.time()) ))