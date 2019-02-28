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
#get_service_date =ttm_graph_processing 'on_demand'
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
gtfsdate = '20190226'
serviceweekstartdate = '20190226'
gtfsdirbase = 'israel'
gtfs_url = 'gtfs.mot.gov.il'
#on OTM (TransitFeeds) the following can be left blank, e.g. ''
gtfs_file_name_on_mot_server = 'israel-public-transportation.zip' 
#gtfs_zip_file_name=gtfsdirbase+gtfsdate+".zip"
gtfspath = 'gtfs'
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

# line_freq config
freqtpdmin = '60'

# lines_on_street config
areatpdmin = '10'

# muni_fairsharescore config

# muni_score_charts config

# muni_tpd_per_line config

# muni_transitscore config

# tpd_at_stops_per_line config

# tpd_near_trainstops_per_line config 
# meters for stop to be considered near trainstop before editing
neartrainstop = '500.0'
autoeditrefdate = '20181021'

# transitscore config

# transit_time_map config
# curent_or_past is changed to past in the js config file by copyprocessed2website.py when moving website_current to website_past
current_or_past = 'current'
default_coverage_name = 'default'
secondary_custom_coverage_name = 'secondary-cov'
# navitia_docker_compose_file_path = '/home/ec2-user/navitia-docker-compose/'
navitia_docker_compose_file_path = 'assets' 
navitia_docker_compose_file_name = 'docker-israel-custom-instances.yml'
# transit_time_map url config - local or AWS API Getway for Transit Analyst production
# local address should be: "http://localhost:9191"
# time_map_server_url = "https://ll7ijshrc0.execute-api.eu-central-1.amazonaws.com/NavitiaTimeMap/"
time_map_server_url = "http://localhost:9191/"

