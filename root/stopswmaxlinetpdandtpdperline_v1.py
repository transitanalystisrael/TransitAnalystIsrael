#!/usr/bin/env python
# -*- coding: utf-8 -*-

# create stops js file with location and tpdperline and maximum tpd of line
#

print('----------------- create stops js file with location and tpdperline and maximum tpd of line --------------------------')

from datetime import date
from datetime import timedelta
import time
import copy
import csv
import json
from geopy.distance import vincenty
import numpy as np
from pathlib import Path

cwd = Path.cwd()
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#_________________________________
#
def main(gtfsdate, processedpath):
    # input:
    parent_path = cwd.parent / processedpath
    servicedate = gtfsdate
    stopswtpdfile = 'stops_w_tpd_per_line'+'_'+servicedate+'.geojson'
    # output:
    stopswmaxtpd = 'stopswmaxtpd'+'_'+servicedate+'.js'

    gtfspathin = parent_path
    gtfspathout = parent_path

    #
    # load files 
    #

    # >>> load stops_w_tpd_per_line geojson file 
    print(parent_path / stopswtpdfile)
    with open(parent_path / stopswtpdfile) as sf:
        stops_geo = json.load(sf)
    print('loaded stops_geo, feature count: ', len(stops_geo['features']))
    #print stops_geo

    #
    # process loaded files
    #

    #
    # recreate stop dict 
    #
    stops_dict = {}
    for feature in stops_geo['features']:
        #print feature['geometry']
        #print feature['properties']
        stop_id = feature['properties']['stop_id']
        stop_lat = feature['geometry']['coordinates'][1]
        stop_lon = feature['geometry']['coordinates'][0]
        maxtpdatstop = feature['properties']['maxtpdatstop']
        averagetpdatstop = feature['properties']['averagetpdatstop']
        maxdaytpdperline_dict = feature['properties']['maxdaytpdperline_dict']
        
        stops_dict[stop_id] = [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict]
    print('len(stops_dict) : ', len(stops_dict))
    #print(maxdaytpdperline_dict) # last one

    # get max tpd
    stopswmaxtpd_dict = {}
    for s_id, [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict] in stops_dict.items():
        max_tpd = 0
        for line_id, tpd in maxdaytpdperline_dict.items() :
            max_tpd = max(max_tpd, tpd)
        stopswmaxtpd_dict[s_id] = max_tpd
    print(stopswmaxtpd_dict)

    #
    #   output js file of stops with location stop_id and max tpd of line
    #

    jsfileout = stopswmaxtpd

    def getJSON(s_id, s_lat, s_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(s_lon),float(s_lat)]
            },
            "properties": { 
                "s_id": s_id,
                "maxtpdatstop": maxtpdatstop, 
                "averagetpdatstop": averagetpdatstop, 
                "maxlinetpdatstop": stopswmaxtpd_dict[s_id],
                "maxdaytpdperline_dict": maxdaytpdperline_dict
            }
        }

    # saveGeoJSON

    print ("Generating GeoJSON export.")
    geoj = {
        "type": "FeatureCollection",
        "features": [getJSON(stop_id, stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict) 
            for stop_id, [stop_lat, stop_lon, maxtpdatstop, averagetpdatstop, maxdaytpdperline_dict] in stops_dict.items()]
    }
    print(("Saving file: ", gtfspathout / jsfileout, " ..."))
    nf = open(gtfspathout / jsfileout, "w", encoding="utf8")
    jsonstr = json.dumps(geoj, separators=(',',':')) # smaller file for download
    outstr = jsonstr.replace('}},', '}},\n')
    nf.write('var stopsWtpdperline =\n')
    nf.write(outstr)
    nf.close()
    print(("Saved file: " + jsfileout))

    print("Local current time :", time.asctime( time.localtime(time.time()) ))
