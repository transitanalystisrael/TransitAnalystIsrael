#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# count the number of trips per day per line at all stops
# in a GTFS file over the selected week of the service period starting at serviceweekstartdate
# include breakdown of tpd per line (agency_id, route short name) at each stop
#
#

import transitanalystisrael_config as cfg
import process_date
import tpd_at_stops_per_line_v2
import time
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
processdate = process_date.get_date_now()

tpd_at_stops_per_line_v2.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, processdate)

print("Local current time :", time.asctime( time.localtime(time.time()) ))