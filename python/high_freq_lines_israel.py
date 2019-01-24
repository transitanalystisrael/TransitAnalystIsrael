#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# count the number of trips per day tpd for all lines (unique routes)
# in a GTFS file over the first week of the entire service period
# merge routes that are the same line using route short name and agency and route decription and direction
# also collect set of stops per route and use to measure common stops between routes that are the same line for a histogram
#
# outputs:
#   txt file of routes with tripcount and stops count - 'routeswtripcountperday.txt'
#   txt file of unique routes - 'uniquerouteswtripcountat'+sstarttimename+sstoptimename+'.txt'
#   js file of lines with name max trips per day and shape geometry - 'route_freq_at'+sstarttimename+sstoptimename+'_'+sstartservicedate+'.js'
#   txt file for histogram of samestops for route_id pairs - samestopshist.txt
#
print '----------------- count the number of trips per day tpd for all lines (unique routes) --------------------------'
print 'generate js file of routes with name max trips per day and shape geometry'
import high_freq_lines_w_tpd_v7
import time
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
#def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout, sstarttime, sstoptime, freqtpdmin):
#
high_freq_lines_w_tpd_v7.main('20181021', 'C:\\transitanalyst\\gtfs\\', 'israel', 'C:\\transitanalyst\\processed\\', '00:00:00', '24:00:00', 60)
print "Local current time :", time.asctime( time.localtime(time.time()) )