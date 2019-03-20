#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# copy and rename files from processed dir to website_current dir or website_yyyymmdd dir for on demand date
# output js file gtfs_start_date.js to folder docs to use as date in the web tools regardless if website_yyyymmdd, website_current or website_past
#
import transitanalystisrael_config as cfg
import process_date
import shutil
import os
import utils
from pathlib import Path

cwd = Path.cwd()

processdate = process_date.get_date_now()
jsfileout = 'gtfs_start_date.js'

no_data_dir = cwd.parent / cfg.websitelocalnodatapath
current_dir = cwd.parent / cfg.websitelocalcurrentpath
past_dir = cwd.parent / cfg.websitelocalpastpath
on_demand_dir = cwd.parent / cfg.websitelocalondemandpath.replace('yyyymmdd', cfg.gtfsdate)
print ('no_data_dir = ',no_data_dir)
print ('current_dir = ',current_dir)
print ('past_dir = ',past_dir)
print ('on_demand_dir = ',on_demand_dir)
print ('cfg.get_service_date = ',cfg.get_service_date)

srcdir = cwd.parent / cfg.processedpath
if cfg.get_service_date == 'auto' : 
	dstdir = current_dir

	os.chdir(srcdir)
	#
	# remove website_past dir
	#
	shutil.rmtree(past_dir)
	#
	# rename website_current dir to website_past
	#
	print('os.rename(current_dir, past_dir)')
	print(current_dir)
	print(past_dir)
	#os.rename(current_dir, past_dir)
	shutil.move(current_dir, past_dir)

	#
	# create website_current dir from website dir with no_data as template.
	#
	#os.mkdir(dstdir)
	for retry in range(100):
		try:
			shutil.copytree(no_data_dir, dstdir)
			break
		except:
			print("rename failed, retrying...")

	#shutil.copytree(no_data_dir, dstdir)
	print(os.listdir(dstdir))
	
else : # on_demand date
	dstdir = on_demand_dir

	os.chdir(srcdir)

	#
	# create website_yyyymmdd dir from website dir with no_data as template.
	#
	#os.mkdir(dstdir)
	for retry in range(100):
		try:
			shutil.copytree(no_data_dir, dstdir)
			break
		except:
			print("rename failed, retrying...")

	#shutil.copytree(no_data_dir, dstdir)
	print(os.listdir(dstdir))
#
# now add the data files from processed dir and change names to remove dates
#

print('date to remove from file names : ', processdate)
#  lines_on_street
shutil.copyfile(srcdir / ("agency_"+processdate+".js"),dstdir / "lines_on_street" / "agency.js")
shutil.copyfile(srcdir / ("route_freq_at_0000-2400_"+processdate+"jerusalem.js"),dstdir / "lines_on_street" / "route_freq_jerusalem.js")
shutil.copyfile(srcdir / ("route_freq_at_0000-2400_"+processdate+"north.js"),dstdir / "lines_on_street" / "route_freq_north.js")
shutil.copyfile(srcdir / ("route_freq_at_0000-2400_"+processdate+"south.js"),dstdir / "lines_on_street" / "route_freq_south.js")
shutil.copyfile(srcdir / ("route_freq_at_0000-2400_"+processdate+"telavivmetro.js"),dstdir / "lines_on_street" / "route_freq_telavivmetro.js")
#line_freq
shutil.copyfile(srcdir / ("agency_"+processdate+".js"),dstdir / "line_freq" / "agency.js")
shutil.copyfile(srcdir / ("route_freq_at_0000-2400_"+processdate+".js"),dstdir / "line_freq" / "route_freq.js")
#muni_fairsharescore
shutil.copyfile(srcdir / ("israel_city_boarders_w_properties_"+processdate+"_"+processdate+".js"),dstdir / "muni_fairsharescore" / "israel_city_boarders_w_properties.js")
shutil.copyfile(srcdir / ("israel_town_boarders_w_properties_"+processdate+"_"+processdate+".js"),dstdir / "muni_fairsharescore" / "israel_town_boarders_w_properties.js")
#muni_score_lists_and_charts
shutil.copyfile(srcdir / ("muni_builtdensityscore_xy.js"),dstdir / "muni_score_lists_and_charts" / "muni_builtdensityscore_xy.js")
shutil.copyfile(srcdir / ("muni_fairsharescore_xy.js"),dstdir / "muni_score_lists_and_charts" / "muni_fairsharescore_xy.js")
shutil.copyfile(srcdir / ("muni_transitscore_xy.js"),dstdir / "muni_score_lists_and_charts" / "muni_transitscore_xy.js")
#muni_tpd_per_line
shutil.copyfile(srcdir / ("agency_"+processdate+".js"),dstdir / "muni_tpd_per_line" / "agency.js")
shutil.copyfile(srcdir / ("israel_city_boarders_w_properties_"+processdate+"_"+processdate+".js"),dstdir / "muni_tpd_per_line" / "israel_city_boarders_w_properties.js")
shutil.copyfile(srcdir / ("israel_town_boarders_w_properties_"+processdate+"_"+processdate+".js"),dstdir / "muni_tpd_per_line" / "israel_town_boarders_w_properties.js")
shutil.copyfile(srcdir / ("muni_w_tpd_per_line_"+processdate+".js"),dstdir / "muni_tpd_per_line" / "muni_w_tpd_per_line.js")
#muni_transitscore
shutil.copyfile(srcdir / ("israel_city_boarders_w_properties_"+processdate+"_"+processdate+".js"),dstdir / "muni_transitscore" / "israel_city_boarders_w_properties.js")
shutil.copyfile(srcdir / ("israel_town_boarders_w_properties_"+processdate+"_"+processdate+".js"),dstdir / "muni_transitscore" / "israel_town_boarders_w_properties.js")
#stops_near_trainstops_editor
shutil.copyfile(srcdir / ("agency_"+processdate+".js"),dstdir / "stops_near_trainstops_editor" / "agency.js")
shutil.copyfile(srcdir / ("stopsneartrainstop_pre_edit_"+processdate+".js"),dstdir / "stops_near_trainstops_editor" / "stopsneartrainstop_pre_edit.js")
shutil.copyfile(srcdir / ("stops_"+processdate+".js"),dstdir / "stops_near_trainstops_editor" / "stops.js")
shutil.copyfile(srcdir / ("trainstop_w_tpd_per_line_"+processdate+".js"),dstdir / "stops_near_trainstops_editor" / "trainstop_w_tpd_per_line.js")
shutil.copyfile(srcdir / ("train_stops_"+processdate+".js"),dstdir / "stops_near_trainstops_editor" / "train_stops.js")
#tpd_at_stops_per_line
shutil.copyfile(srcdir / ("agency_"+processdate+".js"),dstdir / "tpd_at_stops_per_line" / "agency.js")
shutil.copyfile(srcdir / ("stops_w_tpd_per_line_"+processdate+"_"+processdate+".js"),dstdir / "tpd_at_stops_per_line" / "stops_w_tpd_per_line.js")
#tpd_near_trainstops_per_line
shutil.copyfile(srcdir / ("agency_"+processdate+".js"),dstdir / "tpd_near_trainstops_per_line" / "agency.js")
shutil.copyfile(srcdir / ("stopswtrainstopids_"+processdate+".js"),dstdir / "tpd_near_trainstops_per_line" / "stopswtrainstopids.js")
shutil.copyfile(srcdir / ("trainstop_w_tpd_per_line_"+processdate+".js"),dstdir / "tpd_near_trainstops_per_line" / "trainstop_w_tpd_per_line.js")
shutil.copyfile(srcdir / ("train_stops_"+processdate+".js"),dstdir / "tpd_near_trainstops_per_line" / "train_stops.js")
#transitscore
shutil.copyfile(srcdir / ("israel_city_boarders.js"),dstdir / "transitscore" / "israel_city_boarders.js")
shutil.copyfile(srcdir / ("israel_town_boarders.js"),dstdir / "transitscore" / "israel_town_boarders.js")
shutil.copyfile(srcdir / ("ts_lookup_israel"+processdate+".js"),dstdir / "transitscore" / "ts_lookup.js")
shutil.copyfile(srcdir / ("ts_rendered_israel"+processdate+".png"),dstdir / "transitscore" / "ts_rendered.png")

print(os.listdir(dstdir))

#
# output js file gtfs_start_date.js to folder docs to use as date in the web tools regardless if website_yyyymmdd, website_current or website_past
#
fileout = open(dstdir / "docs" / jsfileout, 'w', encoding="utf8") # save results in file
postsline = 'var gtfs_start_date = "'+processdate+'"\n'
print(postsline)
fileout.write(postsline)
fileout.close()
print('saved file: ', str(dstdir / "docs"  / jsfileout))

if cfg.get_service_date == 'auto' : 
	#
	# curent_or_past is changed to past in the js config file that was moved to website_past. TTM needs this to point the client to the correct server
	#
	jsdir = 'docs'
	jsfile = 'transitanalystisrael_config.js'
	tempjsfile = 'temp_config.js'
	in_dir = past_dir / jsdir
	out_dir = past_dir / jsdir
	maxfilelinecount = 2000
	print('input from ', in_dir / jsfile)
	print('output to ', out_dir / tempjsfile)
	if os.path.exists(in_dir / jsfile):
		filein = open(in_dir / jsfile, 'r', encoding="utf8")
		fileout = open(out_dir / tempjsfile, 'w', encoding="utf8")
		count = 0
		sline = filein.readline()
		while ((count < maxfilelinecount) and (sline != '')):
			if sline.find('var cfg_current_or_past') == 0 : 
				postsline = sline.replace("'current'","'past'")
				fileout.write(postsline)
			else :
				postsline = sline
				fileout.write(postsline)
			#print len(sline), sline
			count +=1
			sline = filein.readline()
		print('------------------')
		print(' infile line count ',count)
		filein.close()
		fileout.close()
		print('closed ', in_dir / jsfile)
		print('closed ', out_dir / tempjsfile)
		shutil.copyfile(out_dir / tempjsfile,out_dir / jsfile)
		os.remove(out_dir / tempjsfile)
	else :
		print (in_dir / jsfile, ' does not exist')

#
# if running on AWS then erase all files from processed dir
#
if utils.is_aws_machine():
	os.chdir(cwd.parent)
	shutil.rmtree(cfg.processedpath)
	os.mkdir(cfg.processedpath)
	os.chdir(cwd.parent / cfg.pythonpath)

'''
# old code for getting to all files in dir...
toolslist = ['lines_on_street', 'line_freq', 'muni_fairsharescore', 'muni_score_lists_and_charts', 'muni_tpd_per_line', 'muni_transitscore', 'stops_near_trainstops_editor', 'tpd_at_stops_per_line', 'tpd_near_trainstops_per_line', 'transitscore']
for tooldir in toolslist:
	print '# ',tooldir
	tooldirfilelist = os.listdir('C:\\transitanalyst\\website alpha\\'+tooldir)
	for filename in tooldirfilelist :
		# print filename
		if filename.endswith(".js") or filename.endswith(".png") or filename.endswith(".txt") or filename.endswith(".csv"):
			#print '  ',filename
			filenameout = filename.replace('_'+cfg.serviceweekstartdate, '')
			filenameout = filenameout.replace('_israel'+cfg.serviceweekstartdate, '')
			filenameout = filenameout.replace('at_0000-2400', '')
			filenameout = filenameout.replace('_.js', '.js')
			#print '    ',filenameout
			filein = srcdir+filename
			fileout = dstdir+tooldir+'//'+filenameout
			shutil.copyfile(filein,fileout)
			#print 'shutil.copyfile(srcdir+"',filename,'",dstdir+"',tooldir,'"+"//"+"',filenameout,'")'
'''