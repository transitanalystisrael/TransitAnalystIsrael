#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert post edit text file to pre edit js file for stops near train station editor
#
print '----------------- convert post edit text file to pre edit js file for stops near train station editor --------------------------'

from datetime import date
from datetime import timedelta
import time
import csv
print "Local current time :", time.asctime( time.localtime(time.time()) )
#_________________________________
#
# input:
parent_path = 'C:\\transitanalyst\\processed\\'
servicedate = '20181021'
post_txt_filein = 'stopsneartrainstop_post_edit'+'_'+servicedate+'.txt'
# output:
pre_js_fileout = 'stopsneartrainstop_pre_edit'+'_'+servicedate+'.js'


gtfspathin = parent_path
gtfspathout = parent_path

# >>> load txt file of stopsneartrainstop post edit
txtfilein = post_txt_filein
stopsneartrainstop = {}
with open(gtfspathin+txtfilein, 'rb') as f:
	reader = csv.reader(f)
	header = reader.next() # ['trainstop_id', 'stop_id']
	print header
	for row in reader:
		#print row
		trainstop_id = row[0]
		stop_id = row[1]
		if trainstop_id in stopsneartrainstop :
			stopsneartrainstop[trainstop_id].append(stop_id)
		else :
			stopsneartrainstop[trainstop_id] = [stop_id]
print stopsneartrainstop[trainstop_id] # last one
print 'stopsneartrainstop loaded. trainstop count ', len(stopsneartrainstop)

# >>> output js file of stopsneartrainstop pre edit
fileoutname = pre_js_fileout
fileout = open(gtfspathout+fileoutname, 'w') # open file to save results 
postsline = 'var nearTrainstops = {\n'
for trainstop_id, stopsnearlist in stopsneartrainstop.iteritems():
	postsline += trainstop_id+': ["'
	for stop_id in stopsnearlist :
		postsline += stop_id+'","'
	postsline = postsline[:-2]
	postsline += '],\n'
postsline = postsline[:-2]
postsline += '\n}'
fileout.write(postsline)
fileout.close()
print 'closed file: ', fileoutname

print "Local current time :", time.asctime( time.localtime(time.time()) )
