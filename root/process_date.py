#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# utility to get process date
#
import transitanalystisrael_config as cfg
import json
from pathlib import Path
import datetime
from datetime import timedelta

cwd = Path.cwd()
parent_path = cwd.parent / cfg.staticpath

# >>> load auto_dates_to_process file 
with open(parent_path / cfg.autodatefile) as cf:
	auto_dates = json.load(cf)
#print (auto_dates)

def get_auto_date(yyyymm) :
	return auto_dates['auto_dates_to_process'][yyyymm]

def get_ondemand_date() :
	return cfg.gtfsdate
	
def get_auto_date_now() :
	datenow = datetime.datetime.now()
	yyyymm = str(datenow.year)+format(datenow.month,'02')
	#print("Local current time :", datenow, yyyymm)
	return get_auto_date(yyyymm)
	
def get_auto_date_nextmonth() :
	datenow = datetime.datetime.now()
	tomorrow = datenow + timedelta(days=1)
	datenextmonth = tomorrow
	while datenextmonth.month == datenow.month :
		datenextmonth += timedelta(days=1)
	nextmonth = str(datenextmonth.year)+format(datenextmonth.month,'02')
	return get_auto_date(nextmonth)
	
def get_date_now() :
	if cfg.get_service_date == 'on_demand' :
		return get_ondemand_date()
	else : # cfg.get_service_date == 'auto'
		return get_auto_date_now()