#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GTFS pre processing
import transitanalystisrael_config as cfg
import process_date
import israel_geo_split
import agency_txt2js
import stops_txt2js
import stop_types

processdate = process_date.get_date_now()

israel_geo_split.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
agency_txt2js.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
stops_txt2js.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
stop_types.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)