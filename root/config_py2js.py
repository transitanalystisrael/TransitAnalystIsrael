#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# convert transitanalystisrael_config.py file to transitanalystisrael_config.js for use by index.html client side js processing
#
import transitanalystisrael_config as cfg
import os
from pathlib import Path

cwd = Path.cwd()

pyfile = 'transitanalystisrael_config.py'
jsfile = 'transitanalystisrael_config.js'
jsdir = 'docs'

out_dir = cwd.parent / cfg.websitelocalnodatapath / jsdir
in_dir = cwd.parent / cfg.pythonpath

maxfilelinecount = 2000
print('input from ', in_dir / pyfile)
print('output to ', out_dir / jsfile)
filein = open(in_dir / pyfile, 'r', encoding="utf8")
fileout = open(out_dir / jsfile, 'w', encoding="utf8")
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
print('------------------')
print(' infile line count ',count)
filein.close()
fileout.close()
print('closed ', in_dir / pyfile)
print('closed ', out_dir / jsfile)

