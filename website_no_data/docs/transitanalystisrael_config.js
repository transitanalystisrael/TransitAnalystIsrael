// #!/usr/bin/env python
// # -*- coding: utf-8 -*-
// #
// # config file for transitanalystisrael tools  
// #
// print '----------------- transitanalystisrael config file loading --------------------------'
// import time
// #
// print "Local current time :", time.asctime( time.localtime(time.time()) )

// # common config
// #gtfsdate = '20181021'
// #serviceweekstartdate = '20181021'
var cfg_gtfsdate = '20190202' ;
var cfg_serviceweekstartdate = '20190202' ;
var cfg_gtfsdirbase = 'israel' ;
var cfg_gtfspath = 'C:\\transitanalyst\\gtfs\\' ;
var cfg_processedpath = 'C:\\transitanalyst\\processed\\' ;
// #processedpath = 'C:\\transitanalyst\\temp\\'
var cfg_websitelocalcurrentpath = 'C:\\gitno\\TransitAnalystIsrael\\website_current\\' ;
var cfg_websitelocalpastpath = 'C:\\gitno\\TransitAnalystIsrael\\website_past\\' ;
var cfg_websitelocalnodatapath = 'C:\\git\\TransitAnalystIsrael\\website_no_data\\' ;
var cfg_pythonpath = 'C:\\git\\TransitAnalystIsrael\\python\\' ;
var cfg_sstarttimeall = '00:00:00' ;
var cfg_sstoptimeall = '24:00:00' ;
var cfg_bigjs2gzip = 500000 ;

// # line_freq config
var cfg_freqtpdmin = 60 ;

// # lines_on_street config
var cfg_areatpdmin = 10 ;

// # muni_fairsharescore config

// # muni_score_charts config

// # muni_tpd_per_line config

// # muni_transitscore config

// # tpd_at_stops_per_line config

// # tpd_near_trainstops_per_line config 
var cfg_neartrainstop = 500.0 ; // meters for stop to be considered near trainstop before editing ;

// # transitscore config

// # transit_time_map config
// # curent_or_past is changed to past in the js config file by copyprocessed2website.py when moving website_current to website_past
var cfg_current_or_past = 'current' ;

// #
// print "Local current time :", time.asctime( time.localtime(time.time()) )