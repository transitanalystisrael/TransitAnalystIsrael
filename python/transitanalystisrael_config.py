#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# config file for the 9 of 10 transitanalystisrael tools (TTM is seperate) 
#
print '----------------- transitanalystisrael config file loading --------------------------'
import time
#
print "Local current time :", time.asctime( time.localtime(time.time()) )

# common config
gtfsdate = '20181021'
serviceweekstartdate = '20181021'
gtfsdirbase = 'israel'
gtfspath = 'C:\\transitanalyst\\gtfs\\'
processedpath = 'C:\\transitanalyst\\processed\\'
websitelocalpath = 'C:\\git\\TransitAnalystIsrael\website\\'
pythonpath = 'C:\\git\\TransitAnalystIsrael\\python\\'
sstarttimeall = '00:00:00'
sstoptimeall = '24:00:00'

# line_freq config
freqtpdmin = 60

# lines_on_street config
areatpdmin = 10

# muni_fairsharescore config

# muni_score_charts config

# muni_tpd_per_line config

# muni_transitscore config

# tpd_at_stops_per_line config

# tpd_near_trainstops_per_line config 
neartrainstop = 500.0 # meters for stop to be considered near trainstop before editing

# transitscore config

#
print "Local current time :", time.asctime( time.localtime(time.time()) )