#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Stops Near Trainstops Pre Edit
import transitanalystisrael_config as cfg
import stopsinmuni_v1


stopsinmuni_v1.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)