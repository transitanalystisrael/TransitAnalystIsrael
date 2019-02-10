#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# gzip big data files for upload to cloud
#
import transitanalystisrael_config as cfg
import shutil
import os
print '********** gzip big data files for upload to cloud *************'
current_dir = cfg.websitelocalcurrentpath
print current_dir

os.chdir(current_dir)

toolslist = ['lines_on_street', 'line_freq', 'muni_fairsharescore', 'muni_score_lists_and_charts', 'muni_tpd_per_line', 'muni_transitscore', 'stops_near_trainstops_editor', 'tpd_at_stops_per_line', 'tpd_near_trainstops_per_line', 'transit_time_map', 'transitscore']
for tooldir in toolslist:
	print '# ',tooldir
	tooldirfilelist = os.listdir(current_dir+tooldir)
	for filename in tooldirfilelist :
		print filename
		#print os.path.getsize(current_dir+tooldir+'\\'+filename)
		filepath = current_dir+tooldir+'\\'+filename
		filesize = os.path.getsize(filepath)
		if filename.endswith(".js") and filesize > cfg.bigjs2gzip:
			print '  ',filepath, filesize
			os.system('"gzip -9 -k -f '+filepath+'"')

print os.listdir(current_dir)

