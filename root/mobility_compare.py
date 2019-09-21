#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mobility_compare for date1 and date2, inputs files for date1 and date2 per poi outputs 2 results files per POI
# input:
#    'cumareapersample_'+muni+servicedate1+poi+'_v7.txt' - files for date1 with cumulative area per TTM-Heatmap sample from -60min to +60min
#    'cumareapersample_'+muni+servicedate2+poi+'_v7.txt' - files for date2 with cumulative area per TTM-Heatmap sample from -60min to +60min
# output:
#   histfileout = 'hist_comp_'+muni_name_clean+'.txt' # file with histogram and cumulative histogram compare
#   statsfileout = 'stats_comp_'+muni_name_clean+'.txt' # file with time samples and statistics compare: min | 25% | 50% | 75% | max
#

import csv
from pathlib import Path
import math
import numpy as np
import time
from copy import deepcopy
import mobility_spectrum_cfg as cfg

    
import json
cwd = Path.cwd()

parent_path = cwd.parent / cfg.processedpath / cfg.mobilitypath

#  input:
sel_muni_name = cfg.sel_muni_name
analysis_locs = cfg.analysis_locs
gtfsdate1 = cfg.gtfsdate1
servicedate1 = cfg.servicedate1
gtfsdate2 = cfg.gtfsdate2
servicedate2 = cfg.servicedate2
analysis_time = cfg.analysis_time
percentofarealist = cfg.percentofarealist
munifilein = cfg.munifilein
muni_built_area = 0.0

muni_name_clean = ''.join(e for e in sel_muni_name if e.isalnum())
print(muni_name_clean)

# output:
histfileout = 'hist_comp_'+muni_name_clean+'.txt' # file with histogram and cumulative histogram compare
statsfileout = 'stats_comp_'+muni_name_clean+'.txt' # file with time samples and statistics compare: min | 25% | 50% | 75% | max
#
# >>> load Muni boarders 
with open(parent_path / munifilein) as cf:
    muni_geo = json.load(cf)
print('loaded muni geo, feature count: ', len(muni_geo['features']))
#print muni_geo
sel_muni_found = False
# for each muni, look for selected muni name
for feature in muni_geo['features']:
    if sel_muni_found : break
    #print feature['properties']
    muni_id = feature['properties']['muni_id']
    muni_name = feature['properties']['muni_name']
    print(muni_name)
    if muni_name == sel_muni_name :
        sel_muni_found = True
        muni_built_area = feature['properties']['built_area']
if not sel_muni_found : 
    print('*********** did not find selected muni :',sel_muni_name)
    sys.exit()
print(muni_built_area)

cumareafilesdict = {} # {servicedate1+analysis_poi_name: cumarea_list, ...}
timefromareadict = {} # {date+poi_name+percentofarea: timefromarealist[0:121], ...}
timefromareasorteddict = {} # {date+poi_name+percentofarea: timefromareasortedlist[0:121], ...}

def load_cumarea_file(txtfilein):
    cumarea_list = []
    with open(parent_path / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60
        #print(header)
        for row in reader:
            #print row
            sample_list =[]
            for i in header :
                sample_list.append(float(row[int(i)]))
            cumarea_list.append(sample_list)
    #print(cumarea_list[0])
    print('cumarea_list loaded. sample count ', len(cumarea_list))
    return cumarea_list
    
def comptimefromarea(dateandpoi, area) :
    #print (dateandpoi, area)
    timefromarealist = []
    cumarea_list = cumareafilesdict[dateandpoi]
    for sample, sample_list in enumerate(cumarea_list) :
        for time, areaattime in enumerate(sample_list) :
            if areaattime < area :
                timefromarea = time
        #print(sample, timefromarea)
        timefromarealist.append(timefromarea)
    #print(timefromarealist)
    return timefromarealist

def main() :
    for analysis_loc_dict in analysis_locs : # for each PoI
        print(analysis_loc_dict)
        #print(analysis_loc_dict['name'], analysis_loc_dict['loc'])
        analysis_loc = analysis_loc_dict['loc']
        analysis_poi_name = analysis_loc_dict['name']

        # input files:
        cumareapersamplefilein1 = 'cumareapersample_'+muni_name_clean+servicedate1+analysis_poi_name+'_v7.txt'
        cumareapersamplefilein2 = 'cumareapersample_'+muni_name_clean+servicedate2+analysis_poi_name+'_v7.txt'
        print(cumareapersamplefilein1)
        print(cumareapersamplefilein2)
        
        # >>> load cum area sample input files
        cumareafilesdict[servicedate1+analysis_poi_name] = load_cumarea_file(cumareapersamplefilein1)
        cumareafilesdict[servicedate2+analysis_poi_name] = load_cumarea_file(cumareapersamplefilein2)
        print('len(cumareafilesdict) : ', len(cumareafilesdict))
        #if len(cumareafilesdict) == 2 : print(cumareafilesdict)
        
        # compare duration time from area to poi for two dates for each sample
        for percentofarea in percentofarealist :
            comp_area = muni_built_area*float(percentofarea)/100.0
            print(servicedate1+analysis_poi_name, comp_area)
            timefromareadict[servicedate1+analysis_poi_name+percentofarea] = comptimefromarea(servicedate1+analysis_poi_name, comp_area)
            print(servicedate2+analysis_poi_name, comp_area)
            timefromareadict[servicedate2+analysis_poi_name+percentofarea] = comptimefromarea(servicedate2+analysis_poi_name, comp_area)
        
    #print(timefromareadict)
    #for datepoiarea, timefromarealist in timefromareadict.items():
    #    print (datepoiarea, str(timefromarealist))
        
    # output stats txt file
    fileoutname = statsfileout
    fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
    postsline = 'datepoiarea,'
    for i in range(121) : 
        postsline += str(i)+','
    postsline = postsline[0:-1]
    postsline += '\n'
    print(postsline)
    fileout.write(postsline)
    for datepoiarea, timefromarealist in timefromareadict.items():
        print (datepoiarea, str(timefromarealist))
        postsline = datepoiarea+','
        for i in range(121) : 
            postsline += str(timefromarealist[i])+','
        postsline = postsline[0:-1]
        postsline += '\n'
        #print(postsline)
        fileout.write(postsline)
    #fileout.close()
    #print('closed file: ', fileoutname)

    for datepoiarea, timefromarealist in timefromareadict.items():
        print(timefromarealist)
        timefromarealist.sort()
        print(timefromarealist)
        timefromareasorteddict[datepoiarea] = timefromarealist

    for datepoiarea, timefromarealist in timefromareasorteddict.items():
        print (datepoiarea, str(timefromarealist))
        postsline = datepoiarea+','
        for i in range(121) : 
            postsline += str(timefromarealist[i])+','
        postsline = postsline[0:-1]
        postsline += '\n'
        #print(postsline)
        fileout.write(postsline)
    fileout.close()
    print('closed file: ', fileoutname)
    
    # output hist txt file
    fileoutname = histfileout
    fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
    hist = []
    histdict = {}
    postsline = 'datepoiarea,'
    for i in range(61) : 
        hist.append(0)
        postsline += str(i)+','
    postsline = postsline[0:-1]
    postsline += '\n'
    print(postsline)
    fileout.write(postsline)
    for datepoiarea, timefromarealist in timefromareadict.items():
        print (datepoiarea, str(timefromarealist))
        postsline = datepoiarea+','
        for i in range(61) :
            hist[i] = 0
        for i in range(121) : 
            hist[timefromarealist[i]] +=1
        histdict[datepoiarea] = deepcopy(hist)
        for i in range(61) : 
            postsline += str(hist[i])+','
        postsline = postsline[0:-1]
        postsline += '\n'
        #print(postsline)
        fileout.write(postsline)
    #fileout.close()
    #print('closed file: ', fileoutname)

    for datepoiarea, histlist in histdict.items():
        print (datepoiarea, str(histlist))
        postsline = datepoiarea+','
        cumhistlist= []
        for i in range(61) :
            if i==0:
                cumhistlist.append(histlist[i])
            else :
                cumhistlist.append(cumhistlist[i-1]+histlist[i])
        for i in range(61) : 
            postsline += str(cumhistlist[i])+','
        postsline = postsline[0:-1]
        postsline += '\n'
        #print(postsline)
        fileout.write(postsline)
    fileout.close()
    print('closed file: ', fileoutname)
