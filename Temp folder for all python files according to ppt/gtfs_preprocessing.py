#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GTFS pre processing
import transitanalystisrael_config as cfg
import israel_geo_split
import agency_txt2js
import stops_txt2js

israel_geo_split.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
agency_txt2js.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
stops_txt2js.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)