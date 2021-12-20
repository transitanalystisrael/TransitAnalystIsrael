#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# add to the GTFS shape file shapes for trips that do not have shapes, based on connecting the locations of the stops in sequence.
# it's not a great shape but better than nothing...
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

    #read gtfs stop_times file
    gtfs_file_in = 'stop_times.txt'
    print('read file ', gtfspathin / gtfs_file_in)
    stop_times_df = pd.read_csv(gtfspathin / gtfs_file_in)
    print(stop_times_df)
    print(stop_times_df.columns)
    
    print('drop unneeded info')
    stop_times_df = stop_times_df.drop(['arrival_time', 'departure_time', 'pickup_type', 'drop_off_type', 'shape_dist_traveled'], axis=1)
    print(stop_times_df)
    print(stop_times_df.columns)
    
    #read gtfs trips file
    gtfs_file_in = 'trips.txt'
    print('read file ', gtfspathin / gtfs_file_in)
    trips_df = pd.read_csv(gtfspathin / gtfs_file_in)
    print(trips_df)
    print(trips_df.columns)
    
    print('drop unneeded info')
    trips1_df = trips_df.drop(['route_id', 'service_id', 'trip_headsign', 'direction_id'], axis=1)
    print(trips1_df)
    print(trips1_df.columns)
    #max_shape_id = max(list(trips1_df['shape_id']))
    #print(max_shape_id)
    
    #read gtfs stops file
    gtfs_file_in = 'stops.txt'
    print('read file ', gtfspathin / gtfs_file_in)
    stops_df = pd.read_csv(gtfspathin / gtfs_file_in)
    print(stops_df)
    print(stops_df.columns)
    
    print('drop unneeded info')
    stops_df = stops_df.drop(['stop_code', 'stop_name', 'stop_desc', 'location_type', 'parent_station', 'zone_id'], axis=1)
    print(stops_df)
    print(stops_df.columns)
    
    # filter out valid shape_id-s from trips_df, leaving only trips with blank, i.e. NaN, shape_id-s
    trips1_df.drop(trips1_df[trips1_df['shape_id'] >= 0].index, inplace = True)
    print(trips1_df)
    print(trips1_df.columns)
    
    print('reset index')
    trips1_df.reset_index(drop = True, inplace = True)
    print(trips1_df)
    print(trips1_df.columns)
    
    trips1_df['shape_id'] = 999999
    trips1_df['shape_id'] = trips1_df['shape_id'] - trips1_df.index
    print(trips1_df)
    
    ## add shape_id by merge of stop_times_df and trips1_df on trip_id. trip_ids that were filtered in trips1_df will be left out of the merged df!
    stop_times_df = pd.merge(stop_times_df, trips1_df, on='trip_id')
    print(stop_times_df)
    
    ## add stop location by merge of stop_times_df and stops_df on stop_id. 
    stop_times_df = pd.merge(stop_times_df, stops_df, on='stop_id')
    print(stop_times_df)  
    
    ## sort by = ['shape_id', 'stop_sequence']
    print("sort by = ['shape_id', 'stop_sequence'] ")
    stop_times_df.sort_values(by = ['shape_id', 'stop_sequence'], ascending = [True, True], inplace = True)
    print(stop_times_df)
    print(stop_times_df.columns)
    
    print('drop unneeded info')
    stop_times_df = stop_times_df.drop(['trip_id', 'stop_id'], axis=1)
    print(stop_times_df)
    print(stop_times_df.columns)
    
    # rename columns to make same at shapes.txt - shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
    missing_shapes_df = stop_times_df.rename(columns=({ 'stop_sequence': 'shape_pt_sequence', 'stop_lat': 'shape_pt_lat', 'stop_lon': 'shape_pt_lon'}), inplace=False)
    # reorder the columns to be the same as in shapes.txt
    missing_shapes_df = missing_shapes_df[['shape_id','shape_pt_lat','shape_pt_lon','shape_pt_sequence']] 
    print(missing_shapes_df)
    print(missing_shapes_df.columns)
    
    #read gtfs shapes file
    gtfs_file_in = 'shapes.txt'
    print('read file ', gtfspathin / gtfs_file_in)
    shapes_df = pd.read_csv(gtfspathin / gtfs_file_in)
    print(shapes_df)
    print(shapes_df.columns)
    
    # append missing shapes df to shapes df
    shapes_df = shapes_df.append(missing_shapes_df, ignore_index = True)
    print(shapes_df)
    print(shapes_df.columns)
    
    # output patched shapes df 
    txtfileout = 'shapes_patched.txt'
    print('output file: ', gtfspathout / txtfileout)
    shapes_df.to_csv(gtfspathout / txtfileout, index = False)
    
    # merge trips1_df with trips_df to add missing shape_id-s to trips_df
    trips_df = pd.merge(trips_df, trips1_df, on='trip_id', how='left')
    print(trips_df)
    print(trips_df.columns)
    # change NaN to 0
    trips_df = trips_df.fillna(0)
    trips_df['shape_id'] = (trips_df['shape_id_x']).astype('int') + (trips_df['shape_id_y']).astype('int')
    trips_df = trips_df.drop(['shape_id_x', 'shape_id_y'], axis=1)
    print(trips_df)
    print(trips_df.columns)
    
    # output patched trips df 
    txtfileout = 'trips_patched.txt'
    print('output file: ', gtfspathout / txtfileout)
    trips_df.to_csv(gtfspathout / txtfileout, index = False)
    
    print("Local current time :", time.asctime( time.localtime(time.time()) ))
    
main(cfg.gtfsdate, cfg.gtfspath, cfg.gtfsdirbase, cfg.gtfspath)