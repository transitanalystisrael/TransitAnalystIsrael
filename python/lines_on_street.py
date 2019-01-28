#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# count the number of trips per day tpd for all lines (unique routes)
# in a GTFS file over the first week of the entire service period
# merge routes that are the same line using route short name and agency and route decription and direction
#
# inputs: (from config file - transitanalyst_config.py)
#   GTFS files in cfg.processedpath/cfg.gtfsdirbase+_areaname+cfg.gtfsdate - e.g. 'C:\\transitanalyst\\processed\\israel_south20181021' (created by GTFS_Israel_geo_split.py)
#   path for output files is cfg.processedpath - e.g. 'C:\\transitanalyst\\processed\\'
#   start and end time set for all day cfg.sstarttimeall, cfg.sstoptimeall - e.g. '00:00:00', '24:00:00'
#   min tpd for output is set at cfg.areatpdmin - e.g. 10
#
# outputs: (from high_freq_lines_w_tpd_v7.main()) the txt files are for debug
#   txt file of routes with tripcount and stops count - 'routeswtripcountperday.txt'
#   txt file of unique routes - 'uniquerouteswtripcountat'+sstarttimename+sstoptimename+'.txt'
#   txt file for histogram of samestops for route_id pairs - samestopshist.txt
#   js files of lines with name max trips per day and shape geometry - 'route_freq_at'+sstarttimename+sstoptimename+'_'+sstartservicedate+areaname+'.js'
#		route_freq_at_0000-2400_yyyymmddtelavivmetro.js
#		route_freq_at_0000-2400_yyyymmddjerusalem.js
#		route_freq_at_0000-2400_yyyymmddnorth.js
#		route_freq_at_0000-2400_yyyymmddsouth.js
#
print '----------------- count the number of trips per day tpd for all lines (unique routes) --------------------------'
print 'generate js file of routes with name trips per day and shape geometry'
import transitanalystisrael_config as cfg
import high_freq_lines_w_tpd_v7
import time
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
#def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout, sstarttime, sstoptime, freqtpdmin):
#
high_freq_lines_w_tpd_v7.main(cfg.gtfsdate, cfg.processedpath, cfg.gtfsdirbase+'_south', cfg.processedpath, cfg.sstarttimeall, cfg.sstoptimeall, cfg.areatpdmin)
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
#def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout, sstarttime, sstoptime, freqtpdmin):
#
high_freq_lines_w_tpd_v7.main(cfg.gtfsdate, cfg.processedpath, cfg.gtfsdirbase+'_north', cfg.processedpath, cfg.sstarttimeall, cfg.sstoptimeall, cfg.areatpdmin)
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
#def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout, sstarttime, sstoptime, freqtpdmin):
#
high_freq_lines_w_tpd_v7.main(cfg.gtfsdate, cfg.processedpath, cfg.gtfsdirbase+'_jerusalem', cfg.processedpath, cfg.sstarttimeall, cfg.sstoptimeall, cfg.areatpdmin)
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
#def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout, sstarttime, sstoptime, freqtpdmin):
#
high_freq_lines_w_tpd_v7.main(cfg.gtfsdate, cfg.processedpath, cfg.gtfsdirbase+'_telavivmetro', cfg.processedpath, cfg.sstarttimeall, cfg.sstoptimeall, cfg.areatpdmin)
print "Local current time :", time.asctime( time.localtime(time.time()) )