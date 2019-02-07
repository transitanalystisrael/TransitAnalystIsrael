// #!/usr/bin/env python
// # -*- coding: utf-8 -*-
// #
// # config file for the 9 of 10 transitanalystisrael tools (TTM is seperate) 
// #
// print '----------------- transitanalystisrael config file loading --------------------------'
// import time
// #
// print "Local current time :", time.asctime( time.localtime(time.time()) )

// # common config
var cfg_gtfsdate = '20190202' ;
var cfg_serviceweekstartdate = '20190202' ;
var cfg_gtfsdirbase = 'israel' ;
var cfg_gtfspath = 'C:\\transitanalyst\\gtfs\\' ;
var cfg_processedpath = 'C:\\transitanalyst\\processed\\' ;
// #processedpath = 'C:\\transitanalyst\\temp\\'
var cfg_websitelocalpath = 'C:\\gitno\\TransitAnalystIsrael\website\\' ;
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

// #
// print "Local current time :", time.asctime( time.localtime(time.time()) )