#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Patch new rail routes.txt file to be able to use in TransitAnalystIsrael.
# for changes in rail data see - GTFS_Developer_Information_2021.08.03.pdf
#
# patches:
# - add route_short_name based on train line end stations (derived from route_long_name)
#    - from rout_long_name create lookup table with a two digit code per train end station. 
#    - concatenate origin and destination station codes to create route_short_name
# - add the new route_short_name to the begining 7 characters of the route_desc. 
#    - add the new given 'train number' in the route_desc to fill the last 4 characters of the patched route_desc.
# - add the train number to the route_long_name to make it unique
# 
#
#

import transitanalystisrael_config as cfg
import time
from pathlib import Path
import pandas as pd

cwd = Path.cwd()
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
    # input:
    parent_path = cwd.parent / gtfsparentpath
    gtfsdir = gtfsdirbase+gtfsdate
    
    # output:
    gtfspathout = cwd.parent / pathout / gtfsdir

    
    gtfspathin = parent_path / gtfsdir
    gtfspath = gtfspathin
    
    print("Local current time :", time.asctime( time.localtime(time.time()) ))
    
    #read gtfs routes file
    gtfs_file_in = 'routes.txt'
    print('read file ', gtfspathin / gtfs_file_in)
    routes_df = pd.read_csv(gtfspathin / gtfs_file_in)
    print(routes_df)
    #print(routes_df.columns)
    
    rail_routes_df = routes_df.drop(routes_df[routes_df['agency_id'] != 2].index, inplace = False)
    print(rail_routes_df)
    
    # patch only if routes.txt has new (202108and later) rail routes format and has not been patched. 
    rail_routes_df['len_desc'] = rail_routes_df.apply(lambda row: len(row['route_desc']), axis=1)
    max_len_route_short_name = max(list(rail_routes_df['len_desc']))
    min_len_route_short_name = min(list(rail_routes_df['len_desc']))
    print(min_len_route_short_name, max_len_route_short_name)
    if (max_len_route_short_name > 4) or (min_len_route_short_name > 2) : # return if not new before patch (old old, or old, or patched new)
        return
    rail_routes_df = rail_routes_df.drop(['len_desc'], axis=1)
    
    def split_long_name(row):
        splitted = row['route_long_name'].split('<->')
        return splitted[0], splitted[1]
    # use zip to create the columns
    rail_routes_df['d'], rail_routes_df['o'] = zip(*rail_routes_df.apply(split_long_name, axis=1))
    #print(rail_routes_df)
    
    end_stations_set = set([])
    end_stations_set.update(list(rail_routes_df['o']))
    end_stations_set.update(list(rail_routes_df['d']))
    #print(end_stations_set)
    i=1
    station_lookup_dict = {}
    for station in end_stations_set :
        #print(station)
        station_lookup_dict[station] = str(i).zfill(2)
        i+=1
    #print(station_lookup_dict)
    
    rail_routes_df['o_i'] = rail_routes_df.apply(lambda row: station_lookup_dict[row['o']], axis=1)
    rail_routes_df['d_i'] = rail_routes_df.apply(lambda row: station_lookup_dict[row['d']], axis=1)
    rail_routes_df['route_short_name'] = rail_routes_df['o_i']+'_'+rail_routes_df['d_i']
    rail_routes_df['route_long_name'] = rail_routes_df['route_long_name']+'_'+rail_routes_df['route_desc'].str.zfill(4)
    rail_routes_df['route_desc'] = '_'+rail_routes_df['route_short_name']+'_'+rail_routes_df['route_desc'].str.zfill(4)
    #print(rail_routes_df)
    print('drop unneeded info')
    rail_routes_df = rail_routes_df.drop(['o', 'd', 'o_i', 'd_i'], axis=1)
    print(rail_routes_df)
    
    #replace the rail rows back into the routes df by index
    routes_df.loc[rail_routes_df.index, :] = rail_routes_df[:]
    print(routes_df)
    
    # output patched routes df 
    txtfileout = 'routes.txt'
    print('output file: ', gtfspathout / txtfileout)
    routes_df.to_csv(gtfspathout / txtfileout, index = False)
    
    print("Local current time :", time.asctime( time.localtime(time.time()) ))
    
#main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.gtfspath)