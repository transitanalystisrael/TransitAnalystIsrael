#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import transitanalystisrael_config as cfg
import datetime
import utils

from logger import _log

update_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

try:

	if cfg.get_service_date == 'auto' :
		# get gtfs files and osm file
		_log.info("Download OSM & GTFS")
		import gtfs_osm_download

	#unzip gtfs file
	import gtfs_unzip

	'''
	# copy static files to processed dir
	_log.info("Loading static files")
	import load_static_files

	# process gtfs files to create files in processed dir for use by js in website tools
	_log.info("GTFS pre-processing")
	import gtfs_preprocessing
	# _log.info("Calculating TransitScore Israel")
	import transitscore_israel # check that long processing steps (2 hours)are not commented out in imported file
	_log.info("Calculating Municipal Scores")
	import muni_scores
	_log.info("Calculating High Freq Lines")
	import high_freq_lines_israel
	_log.info("Calculating Lines on Street")
	import lines_on_street
	_log.info("Calculating TPD as stops")
	import tpd_at_stops_israel
	_log.info("Stops in Muni - Pre Edit")
	import stops_in_muni_pre_edit
	_log.info("Stops in Muni - Post Edit")
	import stops_in_muni_pre2post_edit # you can also manually edit the pre file to create the post file and rerun the script with this commented out
	_log.info("Calculating TPD in Municipal")
	import tpd_in_muni_per_line
	_log.info("Stops near train stops - Pre edit")
	import stops_near_trainstops_pre_edit
	_log.info("Stops near train stops - Auto Post edit")
	import trainstopautoeditpre2post_v1 # you can also manually edit the pre file to create the post file and rerun the script with this commented out
	_log.info("TPD near train stops")
	import tpd_near_trainstops_per_line

	# convert the py file to js to use in index.html js code
	_log.info("Convert py config file to js config file")
	import config_py2js

	# copy files from processed dir with date in name to local website dir for testing. rename files to remove date from filenames
	_log.info("Copy processed files to website")
	import copyprocessed2website

	# gzip big data files for upload to cloud
	_log.info("Gzip big files")
	import gzip_big_files

	if cfg.web_client_hosted_on == 'aws_s3' :
		# upload files to cloud website dir from local website dir
		_log.info("Upload website to AWS S3")
		import upload2aws_s3
	'''
	if cfg.ttm_graph_processing != 'none' :
		#process TTM files
		_log.info("Update Navitia Time Map server")
		import navitia_update


# Send e-mail everything is completed - only on automatic script on AWS
# On local Windows machine, there's no need.
except Exception as e:
	if utils.is_aws_machine():
		_log.exception("Done with errors - see Exception stacktrace")
		utils.send_log_to_email("Transit Analyst Monthly Update " + update_time, "Update Failed - see logs")
	else:
		_log.exception("Done with errors - see Exception stacktrace")

