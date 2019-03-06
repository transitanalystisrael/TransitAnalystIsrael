#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# convert stopsinmuni_pre_edit.txt to stopsinmuni_post_edit.txt without any changes
# can be replaced with smart algorithem to deal with edge cases...
#
import transitanalystisrael_config as cfg
import os
from pathlib import Path
import shutil

cwd = Path.cwd()

prefile = 'stopsinmuni_pre_edit_'+cfg.gtfsdate+'.txt'
postfile = 'stopsinmuni_post_edit_'+cfg.gtfsdate+'.txt'

os.chdir(cwd.parent / cfg.processedpath)
shutil.copy(prefile, postfile)


