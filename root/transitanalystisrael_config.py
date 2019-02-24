#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# config file for transitanalystisrael tools  
#
print ('----------------- transitanalystisrael config file loading --------------------------')
import time
import os
#
print ("Local current time :", time.asctime( time.localtime(time.time()) ))

# common config
gtfsdate = '20190202'
serviceweekstartdate = '20190202'
gtfsdirbase = 'israel'
gtfs_url='gtfs.mot.gov.il'
gtfs_file_name_on_mot_server='israel-public-transportation.zip' #on OTM (TransitFeeds) this can be left blank, e.g. ''
# gtfspath = 'C:\\transitanalyst\\gtfs\\'
gtfspath = os.path.join(os.pardir,'gtfs')
gtfs_zip_file_name = 'gtfs_zipped.zip'
# osmpath = 'C:\\transitanalyst\\osm\\'
osmpath = os.path.join(os.pardir, 'osm')
osm_url='https://download.geofabrik.de/asia/israel-and-palestine-latest.osm.pbf'
osm_file_name = "israel-and-palestine-latest.osm.pbf"
staticpath = 'C:\\git\\TransitAnalystIsrael\\static_data\\' 
processedpath = 'C:\\transitanalyst\\processed\\'
#processedpath = 'C:\\transitanalyst\\temp\\'
temppath = 'C:\\transitanalyst\\temp\\'
websitelocalcurrentpath = 'C:\\gitno\\TransitAnalystIsrael\\website_current\\'
websitelocalpastpath = 'C:\\gitno\\TransitAnalystIsrael\\website_past\\'
websitelocalnodatapath = 'C:\\git\\TransitAnalystIsrael\\website_no_data\\'
pythonpath = 'C:\\git\\TransitAnalystIsrael\\root\\'
sstarttimeall = '00:00:00'
sstoptimeall = '24:00:00'
bigjs2gzip = 500000
language = 'hebrew'

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
autoeditrefdate = '20181021'

# transitscore config

# transit_time_map config
# curent_or_past is changed to past in the js config file by copyprocessed2website.py when moving website_current to website_past
current_or_past = 'current'
default_coverage_name='default'
secondary_custom_coverage_name='secondary-cov'
navitia_docker_compose_file_path='assets' #'/home/ec2-user/navitia-docker-compose/'
navitia_docker_compose_file_name='docker-israel-custom-instances.yml'
# transit_time_map url config - local or AWS API Getway for Transit Analyst production
# local address should be: "http://localhost:9191"
time_map_server_url = "https://ll7ijshrc0.execute-api.eu-central-1.amazonaws.com/NavitiaTimeMap/"

#
print ("Local current time :", time.asctime( time.localtime(time.time())))