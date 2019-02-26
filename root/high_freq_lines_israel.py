#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# count the number of trips per day tpd for all lines (unique routes)
# in a GTFS file over the first week of the entire service period
# merge routes that are the same line using route short name and agency and route decription and direction
#
# inputs: (from config file - transitanalyst_config.py)
#   GTFS files in cfg.gtfspath/cfg.gtfsdirbase+cfg.gtfsdate - e.g. 'C:\\transitanalyst\\gtfs\\israel20181021'
#   path for output files is cfg.processedpath - e.g. 'C:\\transitanalyst\\processed\\'
#   start and end time set for all day cfg.sstarttimeall, cfg.sstoptimeall - e.g. '00:00:00', '24:00:00'
#   min tpd for output is set at cfg.freqtpdmin - e.g. 60
#
# outputs: (from high_freq_lines_w_tpd_v7.main()) the txt files are for debug
#   txt file of routes with tripcount and stops count - 'routeswtripcountperday.txt'
#   txt file of unique routes - 'uniquerouteswtripcountat'+sstarttimename+sstoptimename+'.txt'
#   txt file for histogram of samestops for route_id pairs - samestopshist.txt
#   js file of lines with name max trips per day and shape geometry - 'route_freq_at'+sstarttimename+sstoptimename+'_'+sstartservicedate+'.js'
#
print('----------------- count the number of trips per day tpd for all lines (unique routes) --------------------------')
print('generate js file of routes with name max trips per day and shape geometry')
import transitanalystisrael_config as cfg
import high_freq_lines_w_tpd_v7
import time
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
#def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout, sstarttime, sstoptime, freqtpdmin):
#high_freq_lines_w_tpd_v7.main('20181021', 'C:\\transitanalyst\\gtfs\\', 'israel', 'C:\\transitanalyst\\processed\\', '00:00:00', '24:00:00', 60)
#

high_freq_lines_w_tpd_v7.main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath, cfg.sstarttimeall, cfg.sstoptimeall, cfg.freqtpdmin)

print("Local current time :", time.asctime( time.localtime(time.time()) ))