#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# collect a set of trip_id s at all stops in a GTFS file over the selected week of the service period starting at serviceweekstartdate
# filter stops near trainstations based on input txt file - stopsneartrainstop_post_edit
# merge sets of trips at stops near each trainstation to count trips per hour and per day
#
#

import transitanalystisrael_config as cfg
import trip_ids_at_stops_merge_in_muni_perday_v5
import time
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
#

trip_ids_at_stops_merge_in_muni_perday_v5.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, cfg.serviceweekstartdate)

print("Local current time :", time.asctime( time.localtime(time.time()) ))