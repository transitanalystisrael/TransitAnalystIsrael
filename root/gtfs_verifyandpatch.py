#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# check GTFS files for inconsistencies and try to patch them with minimal changes
# e.g. a trip that references a route_id that does not exist in routes.txt (found in GTFS Israel file with start service date of 21 March 2019)
#
# most of the patches are now only placeholders... need to add...
# need to rerun after patch to see that nothing was broken by fix... this is not done yet
#
import transitanalystisrael_config as cfg
import gtfs_config
import time
import csv
from pathlib import Path
from logger import _log

cwd = Path.cwd()
#
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#
def main(gtfsdate, gtfsparentpath, gtfsdirbase, pathout):
    # input:
    parent_path = cwd.parent / gtfsparentpath
    gtfsdir = gtfsdirbase+gtfsdate
    txtfilein = ''
    
    # output:
    gtfspathout = cwd.parent / pathout / gtfsdir
    txtfileout = ''
    
    gtfspathin = parent_path / gtfsdir
    gtfspath = gtfspathin
    
    # >>> load routes file
    routes_count = 0
    txtfilein = 'routes.txt'
    routes_dict = {}
    with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # [route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_color]
        #print(header)
        for row in reader:
            #print row
            routes_count +=1
            routes_dict[row[0]] = [row[1]] # 'route_id' : ['agency_id']
    #print routes_dict[:4]
    print('routes_dict loaded. routes count ', len(routes_dict))
    
    # >>> load trips file
    trips_count = 0
    trips_header_trip_headsign_missing = False
    txtfilein = 'trips.txt'
    trips_dict = {}
    with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
        if len(header) == 5 and header[3] == 'direction_id' : # trip_headsign missing
            trips_header_trip_headsign_missing = True
            print('trip_headsign missing')
            print(header)
        #print(header)
        for row in reader:
            #print(row)
            trips_count +=1
            if trips_header_trip_headsign_missing :
                trips_dict[row[2]] = [row[0],row[1],row[4]] # 'trip_id' : ['route_id','service_id','shape_id']
            else :
                trips_dict[row[2]] = [row[0],row[1],row[5]] # 'trip_id' : ['route_id','service_id','shape_id']
    #print trips_dict[:4]
    print('trips_dict loaded. trips count ', len(trips_dict))
    
    # >>> load stop_times file
    stop_times_count = 0
    txtfilein = 'stop_times.txt'
    stop_times_trips_set = set([])
    stop_times_stops_set = set([])
    with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # [trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled]
        #print(header)
        for row in reader:
            #print row
            stop_times_count +=1
            stop_times_trips_set.add(row[0]) # trip_id
            stop_times_stops_set.add(row[3]) # stop_id
    print('stop_times_trips loaded. trips count ', len(stop_times_trips_set))
    print('stop_times_stops loaded. stops count ', len(stop_times_stops_set))
    
    # >>> load stops file
    stops_count = 0
    txtfilein = 'stops.txt'
    stops_dict = {}
    with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'zone_id']
        #print(header)
        for row in reader:
            #print row
            stops_count +=1
            stops_dict[row[0]] = [row[2], row[3], row[4], row[5]] # 'stop_id' : ['stop_name', 'stop_desc', 'stop_lat', 'stop_lon']
    #print stops_dict[row[0]] # last one
    print('stops_dict loaded. stop count ', len(stops_dict))
    
    # >>> load agency file
    agency_count = 0
    txtfilein = 'agency.txt'
    agency_dict = {}
    agency_name_problem_count = 0
    with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url
        print(header)
        for row in reader:
            print(row)
            agency_count +=1
            agency_name = row[1]
            agency_name_clean = agency_name.replace('\"','').replace("\'","")
            if agency_name != agency_name_clean :
                print('agency name problem: ', agency_name, agency_name_clean)
                agency_name_problem_count +=1
                row[1] = agency_name_clean # patch agency name for dict, later it will be written to file
            agency_dict[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6]] # 'agency_id': ['agency_name','agency_url','agency_timezone','agency_lang','agency_phone','agency_fare_url']
    #print agency_dict[row[0]] # last one
    print('agency_dict loaded. agency count ', len(agency_dict))
    print('agency_name_problem_count : ', agency_name_problem_count)
    
    # >>> load shapes file. Actually loads only one point per shape!!! used only as a set of shape_ids
    shapes_count = 0
    txtfilein = 'shapes.txt'
    shapes_dict = {}
    with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
        #print(header)
        for row in reader:
            #print row
            shapes_count +=1
            shapes_dict[row[0]] = [row[1], row[2]] # 'shape_id' : ['shape_pt_lat','shape_pt_lon']
    #print shapes_dict[row[0]] # last one
    print('shapes_dict loaded. shape count ', len(shapes_dict))
    
    # >>> load calendar file
    calendar_count = 0
    txtfilein = 'calendar.txt'
    calendar_dict = {}
    with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # service_id,sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date
        #print(header)
        for row in reader:
            #print row
            calendar_count +=1
            calendar_dict[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]] # ['service_id' : [ 'sunday','monday','tuesday','wednesday','thursday','friday','saturday','start_date','end_date']
    #print calendar_dict[row[0]] # last one
    print('calendar_dict loaded. calendar count ', len(calendar_dict))
    
    
    # >>> process loaded files
    
    # check MAX limits on file line count
    
    if stops_count > gtfs_config.MAX_STOPS_COUNT :
        print('need to abort')
        _log.error('MAX GTFS line count exceeded')
        raise Exception 
    if stop_times_count > gtfs_config.MAX_STOP_TIMES_COUNT :
        print('need to abort')
        _log.error('MAX GTFS line count exceeded')
        raise Exception
    if trips_count > gtfs_config.MAX_TRIPS_COUNT :
        print('need to abort')
        _log.error('MAX GTFS line count exceeded')
        raise Exception
    if shapes_count > gtfs_config.MAX_SHAPES_COUNT :
        print('need to abort')
        _log.error('MAX GTFS line count exceeded')
        raise Exception
    if routes_count > gtfs_config.MAX_ROUTES_COUNT :
        print('need to abort')
        _log.error('MAX GTFS line count exceeded')
        raise Exception
    if agency_count > gtfs_config.MAX_AGENCY_COUNT :
        print('need to abort')
        _log.error('MAX GTFS line count exceeded')
        raise Exception
    if calendar_count > gtfs_config.MAX_CALENDAR_COUNT :
        print('need to abort')
        _log.error('MAX GTFS line count exceeded')
        raise Exception
    
    # >>> process calendar - check that GTFS start date in calendar.txt is as expected - gtfsdate
    service_ok_count = 0
    service_problem_count = 0
    service_problem_list = []
    min_service_date = '21190101'
    for service_id, [sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date] in calendar_dict.items() :
        min_service_date = min(min_service_date, start_date, end_date)
        if start_date >= gtfsdate and end_date >= gtfsdate :
            service_ok_count +=1
        else :
            service_problem_count +=1
            print('service_problem date before expected start date: start_date, end_date, gtfsdate ', service_id, start_date, end_date, gtfsdate)
            service_problem_list.append([service_id, start_date, end_date, gtfsdate])
    print('service_ok_count : ', service_ok_count)
    print('service_problem_count : ', service_problem_count)
    if min_service_date != gtfsdate : # problem
        print('GTFS file start date in calendar.txt is not the same as expected start date : ', min_service_date, gtfsdate)
        print(cfg.patch_calendar)

        if cfg.patch_calendar == 'yes': # problem and patch
            print('patch_calendar') 
            # >>> open and prep output txt file 
            txtfileout = 'calendar.txt'
            print('open file ', gtfspathout / txtfileout)
            fileout = open(gtfspathout / txtfileout, 'w', encoding="utf8") # save results in file
            postsline = 'service_id,sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date\n'
            print(postsline)
            fileout.write(postsline)
            outfilelinecount = 0
            for service_id, [sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date] in calendar_dict.items() :
                if end_date >= gtfsdate : # good
                    if start_date >= gtfsdate : # good
                        pass
                    else: # *** start date problem *** fix entry to start on gtfsdate
                        print('service_problem date before expected start date: start_date, end_date, gtfsdate ', service_id, start_date, end_date, gtfsdate)
                        start_date = gtfsdate
                    # output entry
                    postsline = ','.join([service_id,sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date])+'\n'
                    fileout.write(postsline)
                    outfilelinecount += 1

                else : # *** end date problem *** skip entry
                    print('end date before GTFS date - erase (skip) this calendar entry', end_date, gtfsdate)
            fileout.close()
            print('close file ', gtfspathout / txtfileout)
            print('lines in out file count ', outfilelinecount)

        else : # problem and no patch
            print('need to abort')
            _log.error('GTFS file start date in calendar.txt is not the same as expected start date : %s %s', min_service_date, gtfsdate)
            raise Exception
        raise Exception
    
    # >>> process routes
    routes_agency_id_ok_count = 0
    routes_agency_id_problem_count = 0
    routes_agency_id_problem_list = []
    agencies_referenced_set = set([])
    for route_id, [agency_id] in routes_dict.items() :
        if agency_id in agency_dict :
            routes_agency_id_ok_count +=1
            agencies_referenced_set.add(agency_id)
        else :
            routes_agency_id_problem_count +=1
            print('routes_agency_id_problem : ', route_id, agency_id)
            routes_agency_id_problem_list.append(route_id)
    print('routes_agency_id_ok_count : ', routes_agency_id_ok_count)
    print('routes_agency_id_problem_count : ', routes_agency_id_problem_count)
    print('agencies_referenced_count : ', len(agencies_referenced_set))
    print('agencies_referenced_set : ', agencies_referenced_set)
    
    # >>> process trips
    trips_service_id_ok_count = 0
    trips_service_id_problem_count = 0
    trips_service_id_problem_list = []
    trips_shape_id_ok_count = 0
    trips_shape_id_problem_count = 0
    trips_shape_id_problem_list = []
    trips_route_id_ok_count = 0
    trips_route_id_problem_count = 0
    trips_route_id_problem_list = []
    for trip_id, [route_id,service_id,shape_id] in trips_dict.items() :
        if route_id in routes_dict :
            trips_route_id_ok_count +=1
        else :
            trips_route_id_problem_count +=1
            print('trips_route_id_problem : ', trip_id, route_id)
            trips_route_id_problem_list.append(trip_id)
        if shape_id in shapes_dict :
            trips_shape_id_ok_count +=1
        else :
            trips_shape_id_problem_count +=1
            print('trips_shape_id_problem : ', trip_id, shape_id)
            #print(shapes_dict.keys())
            trips_shape_id_problem_list.append(trip_id)
        if service_id in calendar_dict :
            trips_service_id_ok_count +=1
        else :
            trips_service_id_problem_count +=1
            print('trips_service_id_problem : ', trip_id, service_id)
            trips_service_id_problem_list.append(trip_id)
    print('trips_service_id_ok_count : ', trips_service_id_ok_count)
    print('trips_service_id_problem_count : ', trips_service_id_problem_count)
    print('trips_shape_id_ok_count : ', trips_shape_id_ok_count)
    print('trips_shape_id_problem_count : ', trips_shape_id_problem_count)
    print('trips_route_id_ok_count : ', trips_route_id_ok_count)
    print('trips_route_id_problem_count : ', trips_route_id_problem_count)
    
    # >>> process stop_times
    stoptimes_trip_id_ok_count = 0
    stoptimes_trip_id_problem_count = 0
    stoptimes_trip_id_problem_list = []
    stoptimes_stop_id_ok_count = 0
    stoptimes_stop_id_problem_count = 0
    stoptimes_stop_id_problem_list = []
    for trip_id in stop_times_trips_set :
        if trip_id in trips_dict :
            stoptimes_trip_id_ok_count +=1
        else :
            stoptimes_trip_id_problem_count +=1
            print('stoptimes_trip_id_problem : ', trip_id)
            stoptimes_trip_id_problem_list.append(trip_id)
    for stop_id in stop_times_stops_set :
        if stop_id in stops_dict :
            stoptimes_stop_id_ok_count +=1
        else :
            stoptimes_stop_id_problem_count +=1
            print('stoptimes_stop_id_problem : ', stop_id)
            stoptimes_stop_id_problem_list.append(stop_id)
    print('stoptimes_trip_id_ok_count : ', stoptimes_trip_id_ok_count)
    print('stoptimes_trip_id_problem_count : ', stoptimes_trip_id_problem_count)
    print('stoptimes_stop_id_ok_count : ', stoptimes_stop_id_ok_count)
    print('stoptimes_stop_id_problem_count : ', stoptimes_stop_id_problem_count)
            
    
    # >>> patch problem files
    if agency_name_problem_count > 0 :# patch agency names, in case they include " or ' in the name (happened in GTFS file of 20190901)
        # >>> open and prep output txt file 
        txtfileout = 'agency.txt'
        print('open file ', gtfspathout / txtfileout)
        fileout = open(gtfspathout / txtfileout, 'w', encoding="utf8") # save results in file
        postsline = 'agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url\n'
        print(postsline)
        fileout.write(postsline)
        outfilelinecount = 0
        for agency_id, [agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url] in agency_dict.items() :
            postsline = ','.join([agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url])+'\n'
            fileout.write(postsline)
            outfilelinecount += 1
        fileout.close()
        print('close file ', gtfspathout / txtfileout)
        print('lines in out file count ', outfilelinecount)
    
    if trips_header_trip_headsign_missing :
        print('trips_header_trip_headsign_missing')
        # add dummy '' trip_headsign
        # load full trips.txt file  then apply the patch while writing back.
        
        # >>> load trips file
        txtfilein = 'trips.txt'
        trips_full_list = []
        with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
            reader = csv.reader(f)
            header = next(reader) # [route_id,service_id,trip_id,direction_id,shape_id]
            #print(header)
            for row in reader:
                #print row
                trips_full_list.append([row[0],row[1],row[2],row[3],row[4]]) # [route_id,service_id,trip_id,direction_id,shape_id]
        print('trips_full_list loaded. trips count ', len(trips_full_list))
        
        # >>> open and prep output txt file 
        txtfileout = 'trips.txt'
        print('open file ', gtfspathout / txtfileout)
        fileout = open(gtfspathout / txtfileout, 'w', encoding="utf8") # save results in file
        postsline = 'route_id,service_id,trip_id,trip_headsign,direction_id,shape_id\n'
        print(postsline)
        fileout.write(postsline)
        outfilelinecount = 0
        trip_headsign = ''
        for [route_id,service_id,trip_id,direction_id,shape_id] in trips_full_list :
            postsline = ','.join([route_id,service_id,trip_id,trip_headsign,direction_id,shape_id])+'\n'
            fileout.write(postsline)
            outfilelinecount += 1
        fileout.close()
        print('close file ', gtfspathout / txtfileout)
        print('lines in out file count ', outfilelinecount)

    if routes_agency_id_problem_count != 0 :
        print('routes_agency_id_problem_count : ', routes_agency_id_problem_count)
        # erase routes if agency_id referenced is missing from agency.txt or add unknown agency to agency.txt with the missing id...
        # for now leaving as is
    
    if trips_service_id_problem_count != 0 :
        print('trips_service_id_problem_count : ', trips_service_id_problem_count)
        # erase trips if service_id referenced is missing from calendar.txt or add empty service record to calendar.txt with the missing id...
        # for now doing the first - but checking that the erased trip will not be missed
        # load full trips.txt file  then apply the patch while writing back.
        
        # >>> load trips file
        txtfilein = 'trips.txt'
        trips_full_list = []
        with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
            reader = csv.reader(f)
            header = next(reader) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
            #print(header)
            for row in reader:
                #print row
                trips_full_list.append([row[0],row[1],row[2],row[3],row[4],row[5]]) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
        print('trips_full_list loaded. trips count ', len(trips_full_list))
        
        # >>> open and prep output txt file 
        txtfileout = 'trips.txt'
        print('open file ', gtfspathout / txtfileout)
        fileout = open(gtfspathout / txtfileout, 'w', encoding="utf8") # save results in file
        postsline = 'route_id,service_id,trip_id,trip_headsign,direction_id,shape_id\n'
        print(postsline)
        fileout.write(postsline)
        outfilelinecount = 0
        for [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id] in trips_full_list :
            if trip_id in trips_service_id_problem_list :
                print('trips_service_id_problem : ', trip_id, service_id)
                print('erasing trip_id from trips.txt')
                # check if this trip that we are erasing will be missed
                if trip_id in stop_times_trips_set :
                    print('ooops **************** erased a trip that is referenced in stoptimes.txt : ', trip_id)
            else :
                postsline = ','.join([route_id,service_id,trip_id,trip_headsign,direction_id,shape_id])+'\n'
                fileout.write(postsline)
                outfilelinecount += 1
        fileout.close()
        print('close file ', gtfspathout / txtfileout)
        print('lines in out file count ', outfilelinecount)
    
    if trips_shape_id_problem_count != 0 :
        print('trips_shape_id_problem_count : ', trips_shape_id_problem_count)
        # if shape_id == "" then create shape from sequence of stops and add to shapes.txt with the newly created id...
        # for now leaving as is
    
    if trips_route_id_problem_count != 0 :
        print('trips_route_id_problem_count : ', trips_route_id_problem_count)
        # erase trips if route_id referenced is missing from routes.txt or add unknown route to route.txt with the missing id...
        # for now doing the first - but checking that the erased trip will not be missed
        # load full trips.txt file  then apply the patch while writing back.
        
        # >>> load trips file
        txtfilein = 'trips.txt'
        trips_full_list = []
        with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
            reader = csv.reader(f)
            header = next(reader) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
            #print(header)
            for row in reader:
                #print row
                trips_full_list.append([row[0],row[1],row[2],row[3],row[4],row[5]]) # [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id]
        print('trips_full_list loaded. trips count ', len(trips_full_list))
        
        # >>> open and prep output txt file 
        txtfileout = 'trips.txt'
        print('open file ', gtfspathout / txtfileout)
        fileout = open(gtfspathout / txtfileout, 'w', encoding="utf8") # save results in file
        postsline = 'route_id,service_id,trip_id,trip_headsign,direction_id,shape_id\n'
        print(postsline)
        fileout.write(postsline)
        outfilelinecount = 0
        for [route_id,service_id,trip_id,trip_headsign,direction_id,shape_id] in trips_full_list :
            if trip_id in trips_route_id_problem_list :
                print('trips_route_id_problem : ', trip_id, route_id)
                print('erasing trip_id from trips.txt')
                # check if this trip that we are erasing will be missed
                if trip_id in stop_times_trips_set :
                    print('ooops **************** erased a trip that is referenced in stoptimes.txt : ', trip_id)
            else :
                postsline = ','.join([route_id,service_id,trip_id,trip_headsign,direction_id,shape_id])+'\n'
                fileout.write(postsline)
                outfilelinecount += 1
        fileout.close()
        print('close file ', gtfspathout / txtfileout)
        print('lines in out file count ', outfilelinecount)

    if (stoptimes_trip_id_problem_count != 0) and (patch_stoptimes_trip_id == 'yes') :
        print('stoptimes_trip_id_problem_count : ', stoptimes_trip_id_problem_count)
        # erase stoptimes if trip_id referenced is missing from trips.txt or add dummy trip...
        # for now doing the first 
        # load full stop_times.txt file  then apply the patch while writing back.
        # **** takes too long - replace with pandas code
        
        # >>> load stop_times file
        txtfilein = 'stop_times.txt'
        stop_times_full_list = []
        with open(gtfspathin / txtfilein, newline='', encoding="utf8") as f:
            reader = csv.reader(f)
            header = next(reader) # [trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled]
            #print(header)
            for row in reader:
                #print row
                stop_times_full_list.append(row) 
        print('stop_times_full_list loaded. count ', len(stop_times_full_list))
        
        # >>> open and prep output txt file 
        txtfileout = 'stop_times.txt'
        print('open file ', gtfspathout / txtfileout)
        fileout = open(gtfspathout / txtfileout, 'w', encoding="utf8") # save results in file
        postsline = 'trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled\n'
        print(postsline)
        fileout.write(postsline)
        outfilelinecount = 0
        for [trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled] in stop_times_full_list :
            if trip_id in stoptimes_trip_id_problem_list :
                print('stoptimes_trip_id_problem, erasing stop_time from stop_times.txt : ', trip_id)
            else :
                postsline = ','.join([trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled])+'\n'
                fileout.write(postsline)
                outfilelinecount += 1
        fileout.close()
        print('close file ', gtfspathout / txtfileout)
        print('lines in out file count ', outfilelinecount)

    if stoptimes_stop_id_problem_count != 0 :
        print('stoptimes_stop_id_problem_count : ', stoptimes_stop_id_problem_count)
        # erase stoptimes if stop_id referenced is missing from stops.txt
        # for now leaving as is
    print('=============================================================================')
    
