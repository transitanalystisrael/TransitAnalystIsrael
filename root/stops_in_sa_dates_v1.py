#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# for each sa, filter stops in sa to create stopsinsa dict.
# output stops in sa in files both txt and js
#
#

print('----------------- create files with stops in sa --------------------------')

from datetime import date
from datetime import timedelta
import time
import copy
import csv
import json
from shapely.geometry import shape, Point, Polygon, MultiPolygon
import numpy as np
from pathlib import Path
import transitanalystisrael_config as cfg

cwd = Path.cwd()
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#_________________________________
#
def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
    
    # input:
    parent_path = cwd.parent / pathout
    gtfs_parent_path = cwd.parent / gtfsparentpath
    servicedate = gtfsdate
    gtfsdir = gtfsdirbase+servicedate
    gtfsstopsfile = 'stops.txt'
    safilein = 'pop_and_land_use_by_sa.geojson'

    # output:
    stops_in_sa = 'stops_in_sa'+'_'+servicedate+'.js'
    stops_in_sa_txt = 'stops_in_sa'+'_'+servicedate+'.txt'

    #
    # load files 
    #

    # >>> load stops file
    txtfilein = gtfs_parent_path / gtfsdir / gtfsstopsfile
    stops_list = []
    with open(txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'zone_id']
        print(header)
        for row in reader:
            #print row
            stops_list.append([row[0], row[1], row[2], row[3], float(row[4]), float(row[5]), row[6], row[7], row[8]])
    print(stops_list[0])
    print('stops_list loaded. stop count ', len(stops_list))
    
    # >>> load sa boarders 
    print (parent_path / safilein)
    with open(parent_path / safilein, encoding="utf8") as cf:
        sa_geo = json.load(cf)
    print('loaded sa geo, feature count: ', len(sa_geo['features']))
    #print sa_geo
    
    #
    # process loaded files
    #

    #
    # create stop dict 
    #
    stops_dict = {}
    for [stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type, parent_station, zone_id] in stops_list:
        stops_dict[stop_id] = [float(stop_lat), float(stop_lon)]
    print('len(stops_dict) : ', len(stops_dict))


    #
    # for each sa
    #   filter stops in boarders multipoly 
    #
    sacount = 0
    sasforoutput_dict = {}
    # for each sa 
    for feature in sa_geo['features']:
    # get sa boarders multipoly to use as filter
        #print feature['properties']
        sa_id = feature['properties']['YISHUV_STA']
        print(sa_id, sacount)
        sacount +=1
        sa_boarder_multipoly = shape(feature['geometry']) # get muni boarders multipoly to use as filter
        #print len(feature['geometry']['coordinates']), sa_boarder_multipoly.geom_type
        #print feature['geometry']['coordinates'][0][0][0]
        if not sa_boarder_multipoly.is_valid : 
            sa_boarder_multipoly = sa_boarder_multipoly.buffer(0) # clean multipoly if not valid
            print('cleaned multipoly')

    # filter stops in boarders multipoly 

        stopinsacount = 0
        for stop_id, [stop_lat, stop_lon] in stops_dict.items() :
            stop_loc = Point(stop_lon, stop_lat)
            if sa_boarder_multipoly.contains(stop_loc) :
                if sa_id in sasforoutput_dict:
                    sasforoutput_dict[sa_id].append(stop_id)
                else :
                    sasforoutput_dict[sa_id] = [stop_id]
                #print stop_loc
                stopinsacount +=1
    print('len(sasforoutput_dict) with sas: ', len(sasforoutput_dict))
    #print(sasforoutput_dict[sa_id]) # last one
    
    # output js file of stopsinsa
    fileoutname = stops_in_sa
    fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
    postsline = 'var insas = {\n'
    for sa_id, stopsinsalist in sasforoutput_dict.items():
        postsline += str(sa_id)+': ["'
        for stop_id in stopsinsalist :
            postsline += stop_id+'","'
        postsline = postsline[:-2]
        postsline += '],\n'
    postsline = postsline[:-2]
    postsline += '\n}'
    fileout.write(postsline)
    fileout.close()
    print('closed file: ', fileoutname)

    # output txt file of stopsinsa
    fileoutname = stops_in_sa_txt
    fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
    postsline = 'sa_id,stop_id\n'
    fileout.write(postsline)
    for sa_id, stopsinsalist in sasforoutput_dict.items():
        for stop_id in stopsinsalist :
            postsline = str(sa_id)+','+stop_id+'\n'
            fileout.write(postsline)
    fileout.close()
    print('closed file: ', fileoutname)
    

#main('20200202', cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)

dates_list = [
     '20220206',
     '20220306',
     '20220501',
     '20220605',
     '20220703',
     '20220807',
     '20220904',
     '20221002',
     '20221106',
     '20221204'
]
"""

dates_list = [
     '20220605',
     '20220703',
     '20220807',
     '20220904',
     '20221002',
     '20221106',
     '20221204'
]
"""
for proc_date in dates_list :
    main(proc_date, cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)

print("Local current time :", time.asctime( time.localtime(time.time()) ))
