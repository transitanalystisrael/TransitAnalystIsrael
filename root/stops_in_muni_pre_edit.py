#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Stops In Muni Pre Edit
import transitanalystisrael_config as cfg
import process_date
import stopsinmuni_v1

processdate = process_date.get_date_now()

stopsinmuni_v1.main(processdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)