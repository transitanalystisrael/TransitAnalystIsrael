#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# copy static data files from static_data dir to processed dir 
#
import transitanalystisrael_config as cfg
import shutil
import os

srcdir = cfg.staticpath
dstdir = cfg.processedpath

os.chdir(srcdir)
print(srcdir)
print(dstdir)
print(os.listdir(srcdir))
srcdirfilelist = os.listdir(srcdir)
for filename in srcdirfilelist :
	print(filename)
	filein = srcdir+filename
	fileout = dstdir+filename
	shutil.copyfile(filein,fileout)
print(os.listdir(dstdir))




