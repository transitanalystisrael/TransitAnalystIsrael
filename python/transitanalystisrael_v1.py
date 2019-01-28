#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 

# process gtfs files to create files in processed dir for use by js in website tools
import gtfs_preprocessing
import transitscore_israel
import muni_scores
import high_freq_lines_israel
import lines_on_street
import tpd_at_stops_israel
import stops_in_muni_pre_edit
import stops_in_muni_pre2post_edit # comment this line out if you want to manually edit the pre file to create the post file
import tpd_in_muni_per_line
import stops_near_trainstops_pre_edit
#import stops_near_trainstops_pre2post_edit # comment this line out if you want to manually edit the pre file to create the post file
import tpd_near_trainstops_per_line

# convert the py file to js to use in index.html js code
import config_py2js 

# copy files to local website dir for testing


# gzip files for upload to cloud


# upload files to cloud website dir from local website dir
