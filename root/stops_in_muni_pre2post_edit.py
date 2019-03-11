#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# convert stopsinmuni_pre_edit.txt to stopsinmuni_post_edit.txt without any changes
# can be replaced with smart algorithem to deal with edge cases...
#
import transitanalystisrael_config as cfg
import process_date
import os
from pathlib import Path
import shutil

processdate = process_date.get_date_now()

cwd = Path.cwd()

prefile = 'stopsinmuni_pre_edit_'+processdate+'.txt'
postfile = 'stopsinmuni_post_edit_'+processdate+'.txt'

os.chdir(cwd.parent / cfg.processedpath)
shutil.copy(prefile, postfile)


