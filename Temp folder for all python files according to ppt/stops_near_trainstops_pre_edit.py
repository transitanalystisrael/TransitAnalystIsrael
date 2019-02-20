#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Stops Near Trainstops Pre Edit
import transitanalystisrael_config as cfg
import train_stops_v2
import stopsneartrainstops_v1


train_stops_v2.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)
stopsneartrainstops_v1.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, cfg.neartrainstop)
