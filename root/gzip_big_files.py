#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# gzip big data files for upload to cloud
#
import transitanalystisrael_config as cfg
import shutil
import os
from pathlib import Path

cwd = Path.cwd()
print('********** gzip big data files for upload to cloud *************')

if cfg.get_service_date == 'auto' : 
	gzip_dir = cwd.parent / cfg.websitelocalcurrentpath
else : # cfg.get_service_date == 'on_demand'
	gzip_dir = cwd.parent / cfg.websitelocalondemandpath.replace('yyyymmdd', cfg.gtfsdate)

print(gzip_dir)

os.chdir(gzip_dir)

toolslist = ['lines_on_street', 'line_freq', 'muni_fairsharescore', 'muni_score_lists_and_charts', 'muni_tpd_per_line', 'muni_transitscore', 'stops_near_trainstops_editor', 'tpd_at_stops_per_line', 'tpd_near_trainstops_per_line', 'transit_time_map', 'transitscore']
for tooldir in toolslist:
	print('# ',tooldir)
	tooldirfilelist = os.listdir(gzip_dir / tooldir)
	for filename in tooldirfilelist :
		print(filename)
		#print (os.path.getsize(gzip_dir / tooldir / filename))
		filepath = gzip_dir / tooldir / filename
		filesize = os.path.getsize(filepath)
		if filename.endswith(".js") and filesize > int(cfg.bigjs2gzip) :
			print('  ',filepath, filesize)
			os.system('"gzip -9 -k -f '+str(filepath)+'"')

print(os.listdir(gzip_dir))

