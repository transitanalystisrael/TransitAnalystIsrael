#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# config file for transitanalystisrael tools  
#

# product templates - remove comment from one product
#

#Monthly auto update on AWS EC2 and S3
#get_service_date = 'auto'
#python_processing = 'aws_ec2'
#ttm_graph_processing = 'aws_ec2'
#web_client_hosted_on = 'aws_s3'
#ttm_server_on = 'aws_ec2'

#Monthly auto update on local pc
get_service_date = 'auto'
python_processing = 'local_pc'
ttm_graph_processing = 'local_pc'
web_client_hosted_on = 'local_pc'
ttm_server_on = 'local_pc'

#On demand date on AWS EC2 and S3
#get_service_date = 'on_demand'
#python_processing = 'aws_ec2'
#ttm_graph_processing = 'aws_ec2'
#web_client_hosted_on = 'aws_s3'
#ttm_server_on = 'aws_ec2'

#On demand date on S3 only (no TTM)
#get_service_date = 'on_demand'
#python_processing = 'local_pc'
#ttm_graph_processing = 'none'
#web_client_hosted_on = 'aws_s3'
#ttm_server_on = 'none'

#On demand date on local pc
#get_service_date = 'on_demand'
#python_processing = 'local_pc'
#ttm_graph_processing = 'local_pc'
#web_client_hosted_on = 'local_pc'
#ttm_server_on = 'local_pc'

#On demand date on local pc no TTM
#get_service_date = 'on_demand'
#python_processing = 'local_pc'
#ttm_graph_processing = 'none'
#web_client_hosted_on = 'local_pc'
#ttm_server_on = 'none'


# common config
# note - gtfsdate and serviceweekstartdate must be the same!!! (untill all scripts support different dates...)
gtfsdate = '20230101'
serviceweekstartdate = '20230101'
autodatefile = 'auto_dates_to_process.json'
gtfsdirbase = 'israel'
gtfs_url = 'gtfs.mot.gov.il'
gtfs_url_test = 'gtfs.mot.gov.il\TestGTFS'
gtfs_file_name_on_mot_server = 'israel-public-transportation.zip' 
gtfspath = 'gtfs'
gtfs_url_https = 'https://gtfs.mot.gov.il//gtfsfiles//israel-public-transportation.zip'
osm_url='https://download.geofabrik.de/asia/israel-and-palestine-latest.osm.pbf'
osm_file_name = "israel-and-palestine-latest.osm.pbf"
osmpath = 'osm'
staticpath = 'static_data' 
processedpath = 'processed'
#processedpath = 'temp'
temppath = 'temp'
websitelocalcurrentpath = 'website_current'
websitelocalpastpath = 'website_past'
websitelocalnodatapath = 'website_no_data'
websitelocalondemandpath = 'website_yyyymmdd'
pythonpath = 'root'
sstarttimeall = '00:00:00'
sstoptimeall = '24:00:00'
bigjs2gzip = '500000'
language = 'hebrew'

# verify and patch config. change from 'no' to 'yes' as needed
patch_calendar = 'no'
patch_stoptimes_trip_id = 'no'

# service weight for transitscore and muni_transitscore
train_weight = '10.0'
lrt_weight = '5.0'
brt_weight = '3.0'
funic_weight = '3.0'
cable_weight = '0.25'
bus_weight = '1.0'

# line_freq config
freqtpdmin = '60'

# lines_on_street config
areatpdmin = '10'
areapeakmin = '1'
sstarttimepeak = '07:00:00'
sstoptimepeak = '09:00:00'

# muni_fairsharescore config

# muni_score_charts config

# muni_tpd_per_line config

# muni_transitscore config

# tpd_at_stops_per_line config

# tpd_near_trainstops_per_line config 
# meters for stop to be considered near trainstop before editing
neartrainstop = '500.0'
autoeditrefdate = '20181021'
# set to '0' to skip autoedit, set to '1' to enable autoedit
stops_near_tainstop_auto_edit = '0'

# transitscore config
maxrawtransitscore20230101 = '62899.3'

# transit_time_map config
# curent_or_past is changed to past in the js config file by copyprocessed2website.py when moving website_current to website_past
current_or_past = 'current'
default_coverage_name = 'default'
secondary_custom_coverage_name = 'secondary-cov'
on_demand_coverage_prefix = 'ondemand-'
# transit_time_map url config - local or AWS API Getway for Transit Analyst production
time_map_server_aws_url = "https://enjayfolml.execute-api.eu-central-1.amazonaws.com/NavitiaTimeMap/"
time_map_server_local_url = "http://localhost:9191/v1/coverage/"

# upload to AWS config
bucket_prefix = 'transitanalystisrael-'


