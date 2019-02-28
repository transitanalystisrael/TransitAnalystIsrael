#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# scan agency.txt to create agency dict keyed on agency_id and includes agency name
# output js array for agency name lookup from agency_id in client js application - agency.js
#
import gtfs_config as gtfscfg
from pathlib import Path

cwd = Path.cwd()

def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
	
	# input:
	parent_path = cwd.parent / gtfsparentpath
	gtfsdir = gtfsdirbase+gtfsdate
	
	# output:
	jsfileout = 'agency'+'_'+gtfsdate+'.js'
	
	gtfspathin = parent_path / gtfsdir
	gtfspath = gtfspathin
	gtfspathout = cwd.parent / pathout
	
	maxfilelinecount = gtfscfg.MAX_AGENCY_COUNT
	gtfspath = gtfspathin
	gtfsfile = 'agency.txt'
	inid = 'agency_id'
	agency_dict = {}
	slinelist=[]
	print(gtfspath / gtfsfile)
	filein = open(gtfspath / gtfsfile, 'r', encoding="utf8")
	sline = filein.readline()
	slinelist=sline[:-1].split(",")
	print(slinelist)
	keylist = slinelist
	inid_index = keylist.index(inid)
	agency_id_i = keylist.index('agency_id')
	agency_name_i = keylist.index('agency_name')
	# scan gtfsfile
	count = 0
	sline = filein.readline()
	while ((count < maxfilelinecount) and (sline != '')):
		slinelist=sline[:-1].split(",")
		print(slinelist)
		in_id = slinelist[inid_index]
		# print in_id 
		agency_dict[in_id] = slinelist[agency_name_i]
		count += 1
		sline = filein.readline()
	print('------------------')
	print(agency_dict)
	print('agency lines scanned ', count) 
	filein.close()
	
	#
	# output js file with array for agency name lookup from agency_id in client js application
	#
	fileout = open(gtfspathout / jsfileout, 'w', encoding="utf8") # save results in file
	postsline = 'var agencies = [];\n'
	print(postsline)
	fileout.write(postsline)
	for agency_id, agency_name in agency_dict.items():
		postsline = 'agencies['+agency_id+'] = "'+agency_name+'";\n'
		print(postsline)
		fileout.write(postsline)
	fileout.close()
	print(gtfspathout / jsfileout)
	print('count ', count)


