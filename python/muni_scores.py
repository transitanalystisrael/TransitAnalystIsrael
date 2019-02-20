#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# calculate per muni transitscore, fairsharescore and builtdensityscore and output to files for display on maps, graphs and lists
#

import transitanalystisrael_config as cfg
import muni_tpd_at_stops_v3_w_10x_for_rail
import muni_opd_from_stops_tpd
import muni_transitscore_from_opd_v2
import time
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
#

muni_tpd_at_stops_v3_w_10x_for_rail.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, cfg.serviceweekstartdate)
muni_opd_from_stops_tpd.main(cfg.gtfsdate, cfg.processedpath, cfg.serviceweekstartdate)
muni_transitscore_from_opd_v2.main(cfg.gtfsdate, cfg.processedpath, cfg.serviceweekstartdate, cfg.language)

print "Local current time :", time.asctime( time.localtime(time.time()) )