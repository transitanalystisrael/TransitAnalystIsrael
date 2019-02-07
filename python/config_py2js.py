#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# convert transitanalystisrael_config.py file to transitanalystisrael_config.js for use by index.html client side js processing
#
import transitanalystisrael_config as cfg
import os

pyfile = 'transitanalystisrael_config.py'
jsfile = 'docs\\'+'transitanalystisrael_config.js'

out_dir = cfg.websitelocalpath[:-1]+'_no_data'+'\\'

maxfilelinecount = 2000
print 'input from ', cfg.pythonpath+pyfile
print 'output to ', cfg.websitelocalpath+jsfile
filein = open(cfg.pythonpath+pyfile, 'r')
fileout = open(out_dir+jsfile, 'w')
count = 0
sline = filein.readline()
while ((count < maxfilelinecount) and (sline != '')):
	if len(sline) == 1 : # blank line copy to fileout
		postsline = sline
		fileout.write(postsline)
	elif sline[0] == '#' :
		postsline = '// '+sline
		fileout.write(postsline)
	elif sline[:6] == 'import' :
		postsline = '// '+sline
		fileout.write(postsline)
	elif sline[:5] == 'print' :
		postsline = '// '+sline
		fileout.write(postsline)
	else :
		sline2 = sline.replace('#','; //')
		postsline = 'var cfg_'+sline2[:-1]+' ;\n'
		fileout.write(postsline)
	#print len(sline), sline
	count +=1
	sline = filein.readline()
print '------------------'
print ' infile line count ',count
filein.close()
fileout.close()
print 'closed ', cfg.pythonpath+pyfile
print 'closed ', out_dir+jsfile

