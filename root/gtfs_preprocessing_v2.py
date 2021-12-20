#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GTFS pre processing
import transitanalystisrael_config as cfg
import process_date
import patch_new_rail_routes_v2
import missing_shapes_from_stops_v2
import gtfs_verifyandpatch
import israel_geo_split
import agency_txt2js
import stops_txt2js
import stop_types

processdate = process_date.get_date_now()

patch_new_rail_routes_v2.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.gtfspath)
missing_shapes_from_stops_v2.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.gtfspath)
gtfs_verifyandpatch.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.gtfspath)

israel_geo_split.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
agency_txt2js.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
stops_txt2js.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
stop_types.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
