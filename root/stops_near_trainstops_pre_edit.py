#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Stops Near Trainstops Pre Edit
import transitanalystisrael_config as cfg
import process_date
import train_stops_v2
import stopsneartrainstops_v1

processdate = process_date.get_date_now()

train_stops_v2.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
stopsneartrainstops_v1.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, cfg.neartrainstop)
