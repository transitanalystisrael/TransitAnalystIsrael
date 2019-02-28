#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# copy static data files from static_data dir to processed dir 
#
import transitanalystisrael_config as cfg
import shutil
import os
from pathlib import Path

cwd = Path.cwd()
srcdir = cwd.parent / cfg.staticpath
dstdir = cwd.parent / cfg.processedpath

os.chdir(srcdir)
print(srcdir)
print(dstdir)
print(os.listdir(srcdir))
srcdirfilelist = os.listdir(srcdir)
if not os.path.exists(dstdir):
	os.mkdir(dstdir)
for filename in srcdirfilelist :
	print(filename)
	filein = srcdir / filename
	fileout = dstdir / filename
	shutil.copyfile(filein,fileout)
print(os.listdir(dstdir))




