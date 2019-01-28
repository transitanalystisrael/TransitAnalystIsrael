#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# convert stopsneartrainstop_pre_edit.txt to stopsneartrainstop_post_edit.txt without any changes
# can be replaced with smart algorithem to deal with edge cases...
#
import transitanalystisrael_config as cfg
import os

prefile = 'stopsneartrainstop_pre_edit.txt'
postfile = 'stopsneartrainstop_post_edit.txt'

os.chdir(cfg.processedpath)
os.system('copy '+prefile+' '+postfile)
