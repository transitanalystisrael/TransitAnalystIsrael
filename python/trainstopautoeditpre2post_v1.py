#!/usr/bin/env python
# -*- coding: utf-8 -*-
# stops near train station auto editor pre to post txt file
# find what stops need to be removed in new file by collecting the stops removed in the manual edit of stopsneartrainstop_pre_edit_20181021
#
print '----------------- stops near train station auto editor pre to post txt file --------------------------'
import transitanalystisrael_config as cfg
from datetime import date
from datetime import timedelta
import time
import csv
print "Local current time :", time.asctime( time.localtime(time.time()) )
#_________________________________
#
# input:
parent_path = cfg.processedpath
servicedate = cfg.gtfsdate
refservicedate = cfg.autoeditrefdate
ref_post_txt_filein = 'stopsneartrainstop_post_edit'+'_'+refservicedate+'.txt'
ref_pre_txt_filein = 'stopsneartrainstop_pre_edit'+'_'+refservicedate+'.txt'
pre_txt_filein = 'stopsneartrainstop_pre_edit'+'_'+servicedate+'.txt'
# output:
post_txt_fileout = 'stopsneartrainstop_post_edit'+'_'+servicedate+'.txt'

gtfspathin = parent_path
gtfspathout = parent_path

# >>> load txt file of stopsneartrainstop pre edit reference date
txtfilein = ref_pre_txt_filein
stopsneartrainstop_ref_pre = {}
with open(gtfspathin+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['trainstop_id', 'stop_id']
	print header
	for row in reader:
		#print row
		trainstop_id = row[0]
		stop_id = row[1]
		if trainstop_id in stopsneartrainstop_ref_pre :
			stopsneartrainstop_ref_pre[trainstop_id].append(stop_id)
		else :
			stopsneartrainstop_ref_pre[trainstop_id] = [stop_id]
print stopsneartrainstop_ref_pre[trainstop_id] # last one
print 'stopsneartrainstop_ref_pre loaded. trainstop count ', len(stopsneartrainstop_ref_pre)

# >>> load txt file of stopsneartrainstop post edit reference date
txtfilein = ref_post_txt_filein
stopsneartrainstop_ref_post = {}
with open(gtfspathin+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['trainstop_id', 'stop_id']
	print header
	for row in reader:
		#print row
		trainstop_id = row[0]
		stop_id = row[1]
		if trainstop_id in stopsneartrainstop_ref_post :
			stopsneartrainstop_ref_post[trainstop_id].append(stop_id)
		else :
			stopsneartrainstop_ref_post[trainstop_id] = [stop_id]
print stopsneartrainstop_ref_post[trainstop_id] # last one
print 'stopsneartrainstop_ref_post loaded. trainstop count ', len(stopsneartrainstop_ref_post)

# >>> load txt file of stopsneartrainstop pre edit 
txtfilein = pre_txt_filein
stopsneartrainstop_pre = {}
with open(gtfspathin+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['trainstop_id', 'stop_id']
	print header
	for row in reader:
		#print row
		trainstop_id = row[0]
		stop_id = row[1]
		if trainstop_id in stopsneartrainstop_pre :
			stopsneartrainstop_pre[trainstop_id].append(stop_id)
		else :
			stopsneartrainstop_pre[trainstop_id] = [stop_id]
print stopsneartrainstop_pre[trainstop_id] # last one
print 'stopsneartrainstop_pre loaded. trainstop count ', len(stopsneartrainstop_pre)

# extract set of stops from each ref dict
stopssetpreref = set([])
for trainstop_id, stopsnearlist in stopsneartrainstop_ref_pre.iteritems():
	for stop_id in stopsnearlist :
		stopssetpreref.add(stop_id)
print 'stopssetpreref len : ',len(stopssetpreref)
stopssetpostref = set([])
for trainstop_id, stopsnearlist in stopsneartrainstop_ref_post.iteritems():
	for stop_id in stopsnearlist :
		stopssetpostref.add(stop_id)
print 'stopssetpostref len : ',len(stopssetpostref)
'''
stopssetpre = set([])
for trainstop_id, stopsnearlist in stopsneartrainstop_pre.iteritems():
	for stop_id in stopsnearlist :
		stopssetpre.add(stop_id)
print 'stopssetpre len : ',len(stopssetpre)
'''

# compute set of removed stops from reference sets
removedset = ([])
removedset = stopssetpreref.difference(stopssetpostref)
print 'removedset len : ',len(removedset)

# create post edit dict by itirating on pre and adding to post only if not in removed set
stopsneartrainstop_post = {}
for trainstop_id, stopsnearlist in stopsneartrainstop_pre.iteritems():
	for stop_id in stopsnearlist :
		if stop_id not in removedset : # then add
			if trainstop_id in stopsneartrainstop_post :
				stopsneartrainstop_post[trainstop_id].append(stop_id)
			else :
				stopsneartrainstop_post[trainstop_id] = [stop_id]
		else : # in removed set
			print 'removed : ', stop_id
print 'stopsneartrainstop_post len : ',len(stopsneartrainstop_post)

# >>> output txt file of stopsneartrainstop post edit
fileoutname = post_txt_fileout
fileout = open(gtfspathout+fileoutname, 'w') # open file to save results 
postsline = 'trainstop_id,stop_id\n'
fileout.write(postsline)
count = 0
for trainstop_id, stopsnearlist in stopsneartrainstop_post.iteritems():
	for stop_id in stopsnearlist :
		postsline = trainstop_id+','+stop_id+'\n'
		fileout.write(postsline)
		count +=1
fileout.close()
print 'closed file: ', fileoutname
print 'line count : ',count

print "Local current time :", time.asctime( time.localtime(time.time()) )

