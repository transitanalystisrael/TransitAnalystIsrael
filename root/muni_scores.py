#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# calculate per muni transitscore, fairsharescore and builtdensityscore and output to files for display on maps, graphs and lists
#

import transitanalystisrael_config as cfg
import muni_tpd_at_stops_w_10x5x3x_for_rail_lrt_brt
import muni_opd_from_stops_tpd
import muni_transitscore_from_opd_v2
import time
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
#

#muni_tpd_at_stops_w_10x5x3x_for_rail_lrt_brt.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, cfg.serviceweekstartdate)
muni_opd_from_stops_tpd.main(cfg.gtfsdate, cfg.processedpath, cfg.serviceweekstartdate)
muni_transitscore_from_opd_v2.main(cfg.gtfsdate, cfg.processedpath, cfg.serviceweekstartdate, cfg.language)

print("Local current time :", time.asctime( time.localtime(time.time()) ))