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
var cfg_gtfsdate = '20190202' ;
var cfg_serviceweekstartdate = '20190202' ;
var cfg_gtfsdirbase = 'israel' ;
var cfg_gtfspath = '..\\gtfs\\' ;
var cfg_osmpath = '..\\osm\\' ;
var cfg_staticpath = '..\\static_data\\'  ;
var cfg_processedpath = '..\\processed\\' ;
// #processedpath = 'C:\\transitanalyst\\temp\\'
var cfg_temppath = '..\\temp\\' ;
var cfg_websitelocalcurrentpath = '..\\website_current\\' ;
var cfg_websitelocalpastpath = '..\\website_past\\' ;
var cfg_websitelocalnodatapath = '..\\website_no_data\\' ;
var cfg_pythonpath = '..\\root\\' ;
var cfg_sstarttimeall = '00:00:00' ;
var cfg_sstoptimeall = '24:00:00' ;
var cfg_bigjs2gzip = 500000 ;
var cfg_language = 'hebrew' ;

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
var cfg_autoeditrefdate = '20181021' ;

// # transitscore config

// # transit_time_map config
// # curent_or_past is changed to past in the js config file by copyprocessed2website.py when moving website_current to website_past
var cfg_current_or_past = 'current' ;

// # transit_time_map url config - local or AWS API Getway for Transit Analyst production
// # local address should be: "http://localhost:9191"
var cfg_time_map_server_url = "https://ll7ijshrc0.execute-api.eu-central-1.amazonaws.com/NavitiaTimeMap/" ;

// #
// print "Local current time :", time.asctime( time.localtime(time.time()) )