#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# calculate per muni transitscore, fairsharescore and builtdensityscore and output to files for display on maps, graphs and lists
#

import transitanalystisrael_config as cfg
import process_date
import muni_tpd_at_stops_w_10x5x3x_for_rail_lrt_brt
import muni_opd_from_stops_tpd
import muni_transitscore_from_opd_v2
import time
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
processdate = process_date.get_date_now()

muni_tpd_at_stops_w_10x5x3x_for_rail_lrt_brt.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, processdate)
muni_opd_from_stops_tpd.main(processdate, cfg.processedpath, processdate)
muni_transitscore_from_opd_v2.main(processdate, cfg.processedpath, processdate, cfg.language)

print("Local current time :", time.asctime( time.localtime(time.time()) ))