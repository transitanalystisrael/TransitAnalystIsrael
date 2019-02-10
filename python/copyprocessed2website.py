#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# copy and rename files from processed dir to website_current dir 
#
import transitanalystisrael_config as cfg
import shutil
import os

no_data_dir = cfg.websitelocalnodatapath
current_dir = cfg.websitelocalcurrentpath
past_dir = cfg.websitelocalpastpath

srcdir = cfg.processedpath
dstdir = current_dir

os.chdir(srcdir)
#
# remove website_past dir
#
shutil.rmtree(past_dir)
#
# rename website_current dir to website_past
#
print 'os.rename(current_dir, past_dir)'
print current_dir
print past_dir
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
        print "rename failed, retrying..."



#shutil.copytree(no_data_dir, dstdir)
print os.listdir(dstdir)

#
# now add the data files from processed dir and change names to remove dates
#

'''
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

print 'date to remove from file names : ', cfg.gtfsdate
#  lines_on_street
shutil.copyfile(srcdir+"agency_"+cfg.gtfsdate+".js",dstdir+"lines_on_street"+"//"+"agency.js")
shutil.copyfile(srcdir+"israel_regions.js",dstdir+"lines_on_street"+"//"+"israel_regions.js")
shutil.copyfile(srcdir+"route_freq_at_0000-2400_"+cfg.gtfsdate+"jerusalem.js",dstdir+"lines_on_street"+"//"+"route_freq_jerusalem.js")
shutil.copyfile(srcdir+"route_freq_at_0000-2400_"+cfg.gtfsdate+"north.js",dstdir+"lines_on_street"+"//"+"route_freq_north.js")
shutil.copyfile(srcdir+"route_freq_at_0000-2400_"+cfg.gtfsdate+"south.js",dstdir+"lines_on_street"+"//"+"route_freq_south.js")
shutil.copyfile(srcdir+"route_freq_at_0000-2400_"+cfg.gtfsdate+"telavivmetro.js",dstdir+"lines_on_street"+"//"+"route_freq_telavivmetro.js")
#line_freq
shutil.copyfile(srcdir+"agency_"+cfg.gtfsdate+".js",dstdir+"line_freq"+"//"+"agency.js")
shutil.copyfile(srcdir+"route_freq_at_0000-2400_"+cfg.gtfsdate+".js",dstdir+"line_freq"+"//"+"route_freq.js")
#muni_fairsharescore
shutil.copyfile(srcdir+"israel_city_boarders_w_properties_"+cfg.gtfsdate+"_"+cfg.gtfsdate+".js",dstdir+"muni_fairsharescore"+"//"+"israel_city_boarders_w_properties.js")
shutil.copyfile(srcdir+"israel_town_boarders_w_properties_"+cfg.gtfsdate+"_"+cfg.gtfsdate+".js",dstdir+"muni_fairsharescore"+"//"+"israel_town_boarders_w_properties.js")
#muni_score_lists_and_charts
shutil.copyfile(srcdir+"muni_builtdensityscore_xy.js",dstdir+"muni_score_lists_and_charts"+"//"+"muni_builtdensityscore_xy.js")
shutil.copyfile(srcdir+"muni_fairsharescore_xy.js",dstdir+"muni_score_lists_and_charts"+"//"+"muni_fairsharescore_xy.js")
shutil.copyfile(srcdir+"muni_transitscore_xy.js",dstdir+"muni_score_lists_and_charts"+"//"+"muni_transitscore_xy.js")
#muni_tpd_per_line
shutil.copyfile(srcdir+"agency_"+cfg.gtfsdate+".js",dstdir+"muni_tpd_per_line"+"//"+"agency.js")
shutil.copyfile(srcdir+"israel_city_boarders_w_properties_"+cfg.gtfsdate+"_"+cfg.gtfsdate+".js",dstdir+"muni_tpd_per_line"+"//"+"israel_city_boarders_w_properties.js")
shutil.copyfile(srcdir+"israel_town_boarders_w_properties_"+cfg.gtfsdate+"_"+cfg.gtfsdate+".js",dstdir+"muni_tpd_per_line"+"//"+"israel_town_boarders_w_properties.js")
shutil.copyfile(srcdir+"muni_w_tpd_per_line_"+cfg.gtfsdate+".js",dstdir+"muni_tpd_per_line"+"//"+"muni_w_tpd_per_line.js")
#muni_transitscore
shutil.copyfile(srcdir+"israel_city_boarders_w_properties_"+cfg.gtfsdate+"_"+cfg.gtfsdate+".js",dstdir+"muni_transitscore"+"//"+"israel_city_boarders_w_properties.js")
shutil.copyfile(srcdir+"israel_town_boarders_w_properties_"+cfg.gtfsdate+"_"+cfg.gtfsdate+".js",dstdir+"muni_transitscore"+"//"+"israel_town_boarders_w_properties.js")
#stops_near_trainstops_editor
shutil.copyfile(srcdir+"agency_"+cfg.gtfsdate+".js",dstdir+"stops_near_trainstops_editor"+"//"+"agency.js")
shutil.copyfile(srcdir+"stopsneartrainstop_pre_edit_"+cfg.gtfsdate+".js",dstdir+"stops_near_trainstops_editor"+"//"+"stopsneartrainstop_pre_edit.js")
shutil.copyfile(srcdir+"stops_"+cfg.gtfsdate+".js",dstdir+"stops_near_trainstops_editor"+"//"+"stops.js")
shutil.copyfile(srcdir+"trainstop_w_tpd_per_line_"+cfg.gtfsdate+".js",dstdir+"stops_near_trainstops_editor"+"//"+"trainstop_w_tpd_per_line.js")
shutil.copyfile(srcdir+"train_stops_"+cfg.gtfsdate+".js",dstdir+"stops_near_trainstops_editor"+"//"+"train_stops.js")
#tpd_at_stops_per_line
shutil.copyfile(srcdir+"agency_"+cfg.gtfsdate+".js",dstdir+"tpd_at_stops_per_line"+"//"+"agency.js")
shutil.copyfile(srcdir+"stops_w_tpd_per_line_"+cfg.gtfsdate+"_"+cfg.gtfsdate+".js",dstdir+"tpd_at_stops_per_line"+"//"+"stops_w_tpd_per_line.js")
#tpd_near_trainstops_per_line
shutil.copyfile(srcdir+"agency_"+cfg.gtfsdate+".js",dstdir+"tpd_near_trainstops_per_line"+"//"+"agency.js")
shutil.copyfile(srcdir+"stopswtrainstopids_"+cfg.gtfsdate+".js",dstdir+"tpd_near_trainstops_per_line"+"//"+"stopswtrainstopids.js")
shutil.copyfile(srcdir+"trainstop_w_tpd_per_line_"+cfg.gtfsdate+".js",dstdir+"tpd_near_trainstops_per_line"+"//"+"trainstop_w_tpd_per_line.js")
shutil.copyfile(srcdir+"train_stops_"+cfg.gtfsdate+".js",dstdir+"tpd_near_trainstops_per_line"+"//"+"train_stops.js")
#transitscore
shutil.copyfile(srcdir+"israel_city_boarders.js",dstdir+"transitscore"+"//"+"israel_city_boarders.js")
shutil.copyfile(srcdir+"israel_town_boarders.js",dstdir+"transitscore"+"//"+"israel_town_boarders.js")
shutil.copyfile(srcdir+"ts_lookup_israel"+cfg.gtfsdate+".js",dstdir+"transitscore"+"//"+"ts_lookup.js")
shutil.copyfile(srcdir+"ts_rendered_israel"+cfg.gtfsdate+".png",dstdir+"transitscore"+"//"+"ts_rendered.png")

print os.listdir(dstdir)

#
# curent_or_past is changed to past in the js config file that was moved to website_past. TTM needs this to point the client to the correct server
#
jsfile = 'docs\\'+'transitanalystisrael_config.js'
tempjsfile = 'docs\\'+'temp_config.js'
in_dir = past_dir
out_dir = past_dir
maxfilelinecount = 2000
print 'input from ', in_dir+jsfile
print 'output to ', out_dir+tempjsfile
filein = open(in_dir+jsfile, 'r')
fileout = open(out_dir+tempjsfile, 'w')
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
print '------------------'
print ' infile line count ',count
filein.close()
fileout.close()
print 'closed ', in_dir+jsfile
print 'closed ', out_dir+tempjsfile
shutil.copyfile(out_dir+tempjsfile,out_dir+jsfile)
os.remove(out_dir+tempjsfile)

