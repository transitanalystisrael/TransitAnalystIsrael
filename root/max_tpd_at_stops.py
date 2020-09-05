#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# max tpd of all lines at stop
#
#

import transitanalystisrael_config as cfg
import process_date
import stopswmaxlinetpdandtpdperline_v1
import time
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
processdate = process_date.get_date_now()

stopswmaxlinetpdandtpdperline_v1.main(processdate, cfg.processedpath)

print("Local current time :", time.asctime( time.localtime(time.time()) ))