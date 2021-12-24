#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# for each taz, filter stops in taz to create stopsintaz dict.
# output stops in taz in files both txt and js
#
#

print('----------------- create files with stops in taz --------------------------')

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
    tazfilein = 'taz_arzi_1270.geojson'

    # output:
    stops_in_taz = 'stops_in_taz'+'_'+servicedate+'.js'
    stops_in_taz_txt = 'stops_in_taz'+'_'+servicedate+'.txt'

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
    
    # >>> load taz boarders 
    print (parent_path / tazfilein)
    with open(parent_path / tazfilein, encoding="utf8") as cf:
        taz_geo = json.load(cf)
    print('loaded taz geo, feature count: ', len(taz_geo['features']))
    #print taz_geo
    
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
    # for each taz
    #   filter stops in boarders multipoly 
    #
    tazcount = 0
    tazsforoutput_dict = {}
    # for each taz 
    for feature in taz_geo['features']:
    # get taz boarders multipoly to use as filter
        #print feature['properties']
        taz_id = feature['properties']['TAZ_1270']
        print(taz_id, tazcount)
        tazcount +=1
        taz_boarder_multipoly = shape(feature['geometry']) # get muni boarders multipoly to use as filter
        #print len(feature['geometry']['coordinates']), taz_boarder_multipoly.geom_type
        #print feature['geometry']['coordinates'][0][0][0]
        if not taz_boarder_multipoly.is_valid : 
            taz_boarder_multipoly = taz_boarder_multipoly.buffer(0) # clean multipoly if not valid
            print('cleaned multipoly')
        
        # filter stops in boarders multipoly 
        stopintazcount = 0
        for stop_id, [stop_lat, stop_lon] in stops_dict.items() :
            stop_loc = Point(stop_lon, stop_lat)
            if taz_boarder_multipoly.contains(stop_loc) :
                if taz_id in tazsforoutput_dict:
                    tazsforoutput_dict[taz_id].append(stop_id)
                else :
                    tazsforoutput_dict[taz_id] = [stop_id]
                #print stop_loc
                stopintazcount +=1
    print('len(tazsforoutput_dict) with tazs: ', len(tazsforoutput_dict))
    #print(tazsforoutput_dict[taz_id]) # last one
    
    # output js file of stopsintaz
    fileoutname = stops_in_taz
    fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
    postsline = 'var intazs = {\n'
    for taz_id, stopsintazlist in tazsforoutput_dict.items():
        postsline += str(taz_id)+': ["'
        for stop_id in stopsintazlist :
            postsline += stop_id+'","'
        postsline = postsline[:-2]
        postsline += '],\n'
    postsline = postsline[:-2]
    postsline += '\n}'
    fileout.write(postsline)
    fileout.close()
    print('closed file: ', fileoutname)

    # output txt file of stopsintaz
    fileoutname = stops_in_taz_txt
    fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
    postsline = 'taz_id,stop_id\n'
    fileout.write(postsline)
    for taz_id, stopsintazlist in tazsforoutput_dict.items():
        for stop_id in stopsintazlist :
            postsline = str(taz_id)+','+stop_id+'\n'
            fileout.write(postsline)
    fileout.close()
    print('closed file: ', fileoutname)
    

main('20200202', cfg.gtfspath, cfg.gtfsdirbase, cfg.processedpath)

print("Local current time :", time.asctime( time.localtime(time.time()) ))
