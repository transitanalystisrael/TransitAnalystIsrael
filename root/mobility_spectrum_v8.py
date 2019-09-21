#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Potential Mobility spectrum for +-one hour around selected time of day
# filtered for one muni to use as measure of acessability from all of muni to major opportunity at analysis_loc
#
# changes:
# v4 - split service date to gtfsdate and servicedate - to be able to specify analysis date different from gtfsdate
# v5 - added more analysis locations for rishon le zion
# v6 - changed muni polygons to use built area in muni polygons instead
# v7 - changed input from in-line code to config file
#
import requests
import sys
import json
import csv
from pathlib import Path
from geopy.distance import vincenty
from shapely.geometry import shape, Point, Polygon, MultiPolygon, box
import math
import numpy as np
import time
import mobility_spectrum_cfg as cfg

def main(gtfsdate, servicedate) :
    import json
    cwd = Path.cwd()

    parent_path = cwd.parent / cfg.processedpath / cfg.mobilitypath

    #  input:
    sel_muni_name = cfg.sel_muni_name
    analysis_locs = cfg.analysis_locs
    #gtfsdate = cfg.gtfsdate
    #servicedate = cfg.servicedate
    analysis_time = cfg.analysis_time
    local_url = cfg.local_url
    munifilein = cfg.munifilein
    navitia_server_url = local_url + cfg.on_demand_coverage_prefix + gtfsdate

    navitia_server_url_heat_maps = navitia_server_url +  "/heat_maps"
    resolution = "750"
    number_of_cells = int(resolution)*int(resolution)

    muni_name_clean = ''.join(e for e in sel_muni_name if e.isalnum())
    print(muni_name_clean)

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
        muni_built_area = feature['properties']['built_area']
        print(muni_name)
        if muni_name == sel_muni_name :
            sel_muni_found = True
            muni_boarder_multipoly = shape(feature['geometry']) # get muni boarders multipoly to use as filter
            #print len(feature['geometry']['coordinates']), muni_boarder_multipoly.geom_type
            #print feature['geometry']['coordinates'][0][0][0]
            if not muni_boarder_multipoly.is_valid : 
                muni_boarder_multipoly = muni_boarder_multipoly.buffer(0) # clean multipoly if not valid
                print('cleaned multipoly')
            (minx,miny,maxx,maxy) = muni_boarder_multipoly.bounds
            muni_boundingbox = box(minx,miny,maxx,maxy)
            print(muni_boundingbox)

    if not sel_muni_found : 
        print('*********** did not find selected muni :',sel_muni_name)
        sys.exit()

    print(navitia_server_url_heat_maps)

    for analysis_loc_dict in analysis_locs :
        print(analysis_loc_dict)
        #print(analysis_loc_dict['name'], analysis_loc_dict['loc'])
        analysis_loc = analysis_loc_dict['loc']

        # output:
        mobilityspectrumfileout = 'mobilityspectrum_'+muni_name_clean+servicedate+analysis_loc_dict['name']+'_v7.txt'
        cumareapersamplefileout = 'cumareapersample_'+muni_name_clean+servicedate+analysis_loc_dict['name']+'_v7.txt'
        print(cumareapersamplefileout)
        
        analysis_time_min = int(analysis_time[0:2])*60+int(analysis_time[2:4])
        s = (110,61)
        mobility_spectrum = np.zeros((s), dtype=int)
        print(mobility_spectrum[0])
        s = (121,61)
        cumarea = np.zeros((s), dtype=float)
        max_cum_area = 0.0
        time_loop = 0
        #for time_min in range(analysis_time_min-1,analysis_time_min+2): # for testing with 3 samples instead of 121
        for time_min in range(analysis_time_min-60,analysis_time_min+61):
            stime = str(int(time_min/60)).zfill(2)+str(time_min%60).zfill(2)+'00'
            print(time_min, stime)
            dateTimeString = servicedate+'T'+stime
            
            heatMapJsonUrl = navitia_server_url_heat_maps  + \
                "?max_duration=" + str(60*60) + \
                "&to=" + analysis_loc[1] + \
                "%3B" + analysis_loc[0] + \
                "&datetime=" + dateTimeString + \
                "&resolution=" + resolution
            
            print(heatMapJsonUrl)
            #time.sleep(20)
            response = requests.get(heatMapJsonUrl)
            json = response.json()
            print(response.status_code)
            while response.status_code != 200 :
                time.sleep(20)
                response = requests.get(heatMapJsonUrl)
                json = response.json()
                print(response.status_code)
            print(json.keys())
            heat_matrix = json['heat_maps'][0]['heat_matrix']
            print(heat_matrix.keys())
            print(heat_matrix['line_headers'][0])
            #print(heat_matrix['lines'][0]['duration'])
            #print(heat_matrix['lines'][0]['cell_lon'])
            count = 0
            cell_count = 0
            cum_area = 0.0
            cell_hist = []
            for i in range(61) : cell_hist.append(0)
            for lon_i, line in enumerate(heat_matrix['lines']) :
            #for line in heat_matrix['lines']:
                #print(lon_i,line['cell_lon'])
                #print(line['duration'])
                for lat_i, duration in enumerate(line['duration']):
                    if duration != None :
                        #print(count, duration)
                        cell_lat = heat_matrix['line_headers'][lat_i]['cell_lat']['center_lat']
                        cell_lon = line['cell_lon']['center_lon']
                        #print(lat_i, lon_i, cell_lat, cell_lon)
                        cell_loc = Point(cell_lon, cell_lat)
                        if muni_boundingbox.contains(cell_loc) :
                            if muni_boarder_multipoly.contains(cell_loc) :
                                cell_hist[int(duration/60)] +=1
                                cell_count +=1
                    count +=1
            print(cell_hist)
            
            matrixLat1 = heat_matrix['line_headers'][0]['cell_lat']['min_lat']
            matrixLon1 = heat_matrix['lines'][0]['cell_lon']['min_lon']
            matrixLat2 = heat_matrix['line_headers'][int(resolution)-1]['cell_lat']['max_lat'] 
            matrixLon2 = heat_matrix['lines'][0]['cell_lon']['min_lon']
            matrixLat3 = heat_matrix['line_headers'][int(resolution)-1]['cell_lat']['max_lat'] 
            matrixLon3 = heat_matrix['lines'][int(resolution)-1]['cell_lon']['max_lon']
            matrixLat4 = heat_matrix['line_headers'][0]['cell_lat']['min_lat'] 
            matrixLon4 = heat_matrix['lines'][int(resolution)-1]['cell_lon']['max_lon']
            print(matrixLat1, matrixLon1)
            print(matrixLat2, matrixLon2)
            print(matrixLat3, matrixLon3)
            print(matrixLat4, matrixLon4)
            matrix_loc0 = (matrixLat1, matrixLon1)
            matrix_loc1 = (matrixLat2, matrixLon2)
            matrix_loc2 = (matrixLat3, matrixLon3)
            matrix_loc3 = (matrixLat4, matrixLon4)
            
            len_a = vincenty(matrix_loc0,matrix_loc1).m # in m
            len_b = vincenty(matrix_loc1,matrix_loc2).m 
            len_c = vincenty(matrix_loc2,matrix_loc3).m 
            len_d = vincenty(matrix_loc3,matrix_loc0).m 
            len_h = math.sqrt(math.pow(len_a,2)-math.pow((len_d-len_b)/2,2))
            matrixArea = (len_h * (len_b+len_d)/2 )/1000000 # in SqKm
            print(len_h, matrixArea)
            areapercell = matrixArea/float(number_of_cells)
            print(areapercell, cell_count)
            cum_area = cell_count * areapercell
            max_cum_area = max(max_cum_area, cum_area)
            print(max_cum_area)
            #print(cumarea[0])
            cumarea[time_loop][0] = cell_hist[0]*areapercell
            for i in range(1,61) : 
                cumarea[time_loop][i] = (cell_hist[i]*areapercell+cumarea[time_loop][i-1])
            print(time_loop, cumarea[time_loop])
            time_loop +=1

        print('time_loop done -------------------------------------------------')
        # build mobility spectrum
        #print(cumarea)
        for cumareavec in cumarea :
            print(max_cum_area)
            print(cumareavec)
            cumareaint = []
            for i in range(61) : 
                cumareaint.append(int(100*cumareavec[i]/max_cum_area))
            print(cumareaint)
            for i in range(61) : 
                mobility_spectrum[cumareaint[i]][i] +=1

        # output txt files
        fileoutname = mobilityspectrumfileout
        fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
        postsline = ''
        for i in range(61) : 
            postsline += str(i)+','
        postsline = postsline[0:-1]
        postsline += '\n'
        print(postsline)
        fileout.write(postsline)
        for rowlist in mobility_spectrum:
            postsline = ''
            for i in range(61) : 
                postsline += str(rowlist[i])+','
            postsline = postsline[0:-1]
            postsline += '\n'
            #print(postsline)
            fileout.write(postsline)
        fileout.close()
        print('closed file: ', fileoutname)

        fileoutname = cumareapersamplefileout
        fileout = open(parent_path / fileoutname, 'w', encoding="utf8") # open file to save results 
        postsline = ''
        for i in range(61) : 
            postsline += str(i)+','
        postsline = postsline[0:-1]
        postsline += '\n'
        print(postsline)
        fileout.write(postsline)
        for rowlist in cumarea:
            postsline = ''
            for i in range(61) : 
                postsline += str(rowlist[i])+','
            postsline = postsline[0:-1]
            postsline += '\n'
            #print(postsline)
            fileout.write(postsline)
        fileout.close()
        print('closed file: ', fileoutname)

