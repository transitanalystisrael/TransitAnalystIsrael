#!/usr/bin/env python
#--------------------------------------------------
# filter the GTFS files by a given area keep only trips that start and end in given area
#
# scan stops by lat-lon and create keep_stop_id_set
# scan stop_times by keep_stop_set to create keep_trip_id_set, keep only trips that start stop and end stop are in keep_stop_set
# filter in stop_times by keep_trip_id_set and create full keep_stop_id_set
# filter in stops by keep_stop_id_set
# filter in trips by keep_trip_id_set and create keep_rout_id_set and keep service_id_set and keep shape_id_set
# filter in routes by keep_rout_id_set and create keep_agency_id_set
# filter in agency by keep_agency_id_set
# filter in calendar by keep service_id_set
# filter in shapes by keep_shape_id_set
#--------------------------------------------------
# begin main ------------------------------------
import time;
import GTFS_geo_filter_util_w_circle_w_startendstops
print "Local current time :", time.asctime( time.localtime(time.time()) )

"""
# sample args:

gtfspathin = 'C:\\GTFS\\israel-public-transportation\\'
gtfspathout = 'C:\\GTFS\\israel-public-transportation-ramat-aviv-gimel\\'

geo_filter = [
    (32.13437749119699, 34.78600044250493),
    (32.12798127926025, 34.81260795593266),
    (32.1179499530071, 34.812264633178756),
    (32.12383803904156, 34.7817089080811)]
"""
def main(gtfspathin, gtfspathout, geo_filter):
    #
    MAX_STOPS_COUNT = 50000
    MAX_STOP_TIMES_COUNT = 25000000
    MAX_TRIPS_COUNT = 900000
    MAX_SHAPES_COUNT = 10000000
    MAX_ROUTES_COUNT = 15000
    MAX_AGENCY_COUNT = 100
    MAX_CALENDAR_COUNT = 250000
    #
    keep_stop_set = set([]) # set of 'stop_id'
    keep_trip_set = set([]) # set of  'trip_id'
    keep_route_set = set([]) # set of  'route_id'
    keep_service_set = set([]) # set of  'service_id'
    keep_agency_set = set([]) # set of  'agency_id'
    keep_service_set = set([]) # set of  'service_id'
    keep_shape_set = set([]) # set of  'shape_id'
    #
    #
    # scan stops by lat-lon and create keep_stop_id_set
    keep_stop_set = GTFS_geo_filter_util_w_circle_w_startendstops.scan_stops_by_lat_lon(gtfspathin, gtfspathout, MAX_STOPS_COUNT, geo_filter)
    print "Local current time :", time.asctime( time.localtime(time.time()) )
    # print list(keep_stop_set)[:2], '... ', list(keep_stop_set)[-3:-1]
    #
    # scan stop_times by keep_stop_set to create keep_trip_id_set, keep only trips that start stop and end stop are in keep_stop_set
    keep_trip_set = GTFS_geo_filter_util_w_circle_w_startendstops.collect_trips_w_startandend_stops_in_stop_set(gtfspathin, keep_stop_set)
    print "Local current time :", time.asctime( time.localtime(time.time()) )
    # print list(keep_trip_set)[:8], '... ', list(keep_trip_set)[-9:-1]
    #
    # filter in stop_times by keep_trip_id_set and create full keep_stop_id_set
    keep_stop_set = set([]) # reset set to gen full set of used stops, including stops ouside geo-filter that are on trips with stops in geo-filter
    keep_stop_set = GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfspathout, 'stop_times.txt', MAX_STOP_TIMES_COUNT, keep_trip_set, 'trip_id', 'stop_id')
    print "Local current time :", time.asctime( time.localtime(time.time()) )
    # print list(keep_stop_set)[:8], '... ', list(keep_stop_set)[-9:-1]
    #
    # filter in stops by keep_stop_id_set
    # print filter_stops_by_stop_set(gtfspathin, gtfspathout, keep_stop_set)
    print GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set(gtfspathin, gtfspathout, 'stops.txt', MAX_STOPS_COUNT, keep_stop_set, 'stop_id')
    print "Local current time :", time.asctime( time.localtime(time.time()) )
    #
    # filter in trips by keep_trip_id_set and create keep_route_id_set and keep_service_id_set and keep_shape_id_set
    keep_route_set = GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfspathout, 'trips.txt', MAX_TRIPS_COUNT, keep_trip_set, 'trip_id', 'route_id')
    keep_service_set = GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfspathout, 'trips.txt', MAX_TRIPS_COUNT, keep_trip_set, 'trip_id', 'service_id')
    keep_shape_set = GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfspathout, 'trips.txt', MAX_TRIPS_COUNT, keep_trip_set, 'trip_id', 'shape_id')
    print "Local current time :", time.asctime( time.localtime(time.time()) )
    # print list(keep_route_set)[:8], '... ', list(keep_route_set)[-9:-1]
    # print list(keep_service_set)[:8], '... ', list(keep_service_set)[-9:-1]
    # print list(keep_shape_set)[:8], '... ', list(keep_shape_set)[-9:-1]
    #
    # filter in routes by keep_route_id_set and create keep_agency_id_set
    keep_agency_set = GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfspathout, 'routes.txt', MAX_ROUTES_COUNT, keep_route_set, 'route_id', 'agency_id')
    print "Local current time :", time.asctime( time.localtime(time.time()) )
    # print list(keep_agency_set)[:8], '... ', list(keep_agency_set)[-9:-1]
    #
    # filter in agency by keep_agency_id_set
    print GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set(gtfspathin, gtfspathout, 'agency.txt', MAX_AGENCY_COUNT, keep_agency_set, 'agency_id')
    localtime = time.asctime( time.localtime(time.time()) )
    print "Local current time :", localtime
    #
    # filter in calendar by keep_service_id_set
    print GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set(gtfspathin, gtfspathout, 'calendar.txt', MAX_CALENDAR_COUNT, keep_service_set, 'service_id')
    print "Local current time :", time.asctime( time.localtime(time.time()) )
    #
    # filter in shapes by keep_shape_id_set
    print GTFS_geo_filter_util_w_circle_w_startendstops.filter_gtfsfile_by_in_set(gtfspathin, gtfspathout, 'shapes.txt', MAX_SHAPES_COUNT, keep_shape_set, 'shape_id')
    print "Local current time :", time.asctime( time.localtime(time.time()) )

    print len(keep_stop_set), ' items in set of stop_id'
    print len(keep_trip_set), ' items in set of trip_id'
    print len(keep_route_set), ' items in set of route_id'
    print len(keep_service_set), ' items in set of service_id'
    print len(keep_agency_set), ' items in set of agency_id'
    print len(keep_service_set), ' items in set of service_id'
    print len(keep_shape_set), ' items in set of shape_id'
    return
