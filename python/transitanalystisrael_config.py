#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# config file for transitanalystisrael tools  
#
print '----------------- transitanalystisrael config file loading --------------------------'
import time
#
print "Local current time :", time.asctime( time.localtime(time.time()) )

# common config
#gtfsdate = '20181021'
#serviceweekstartdate = '20181021'
gtfsdate = '20190202'
serviceweekstartdate = '20190202'
gtfsdirbase = 'israel'
gtfspath = 'C:\\transitanalyst\\gtfs\\'
processedpath = 'C:\\transitanalyst\\processed\\'
#processedpath = 'C:\\transitanalyst\\temp\\'
temppath = 'C:\\transitanalyst\\temp\\'
websitelocalcurrentpath = 'C:\\gitno\\TransitAnalystIsrael\\website_current\\'
websitelocalpastpath = 'C:\\gitno\\TransitAnalystIsrael\\website_past\\'
websitelocalnodatapath = 'C:\\git\\TransitAnalystIsrael\\website_no_data\\'
pythonpath = 'C:\\git\\TransitAnalystIsrael\\python\\'
sstarttimeall = '00:00:00'
sstoptimeall = '24:00:00'
bigjs2gzip = 500000

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

# transit_time_map config
# curent_or_past is changed to past in the js config file by copyprocessed2website.py when moving website_current to website_past
current_or_past = 'current'

#
print "Local current time :", time.asctime( time.localtime(time.time()) )