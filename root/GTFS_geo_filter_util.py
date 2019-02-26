#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------
# filter the GTFS files by a given area
#
# scan stops by lat-lon and create keep_stop_id_set
# scan stop_times by keep_stop_set to create keep_trip_id_set
# filter in stop_times by keep_trip_id_set and create full keep_stop_id_set
# filter in stops by keep_stop_id_set
# filter in trips by keep_trip_id_set and create keep_rout_id_set and keep service_id_set and keep shape_id_set
# filter in routes by keep_rout_id_set and create keep_agency_id_set
# filter in agency by keep_agency_id_set
# filter in calendar by keep service_id_set
# filter in shapes by keep_shape_id_set
#---------------------------------------------------
#
# scan stops by lat-lon and create keep_stop_id_set
#
# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This fuction
# returns True or False.  The algorithm is called
# "Ray Casting Method".

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
#
## Test
#
# polygon = [(0,10),(10,10),(10,0),(0,0)]
#
# point_x = 5
# point_y = 5
#
## Call the fuction with the points and the polygon
# print point_in_poly(point_x,point_y,polygon

#
# collect out set of stop ids from stops.txt of stops inside geo_filter polygon and write lines of inside stops to stops.txt file out
#
def scan_stops_by_lat_lon(gtfspathin, gtfspathout, maxfilelinecount,geo_filter_poly):
    gtfsfile = 'stops.txt'
    outsetid = 'stop_id'
    outset_id = 'string of text'
    stop_lat = 0.0
    stop_lon = 0.0
    slinelist=[]
    postsline = ''
    print('scan_stops_by_lat_lon')
    print(gtfspathin+gtfsfile)
    out_set = set([])
    filein = open(gtfspathin+gtfsfile, 'r', encoding="utf8")
    fileout = open(gtfspathout+gtfsfile, 'w', encoding="utf8")
    sline = filein.readline()
    fileout.write(sline)
    sline = sline[:-1]
    slinelist=sline.split(",")
    outset_id_index = slinelist.index(outsetid)
    stop_lat_index = slinelist.index("stop_lat")
    stop_lon_index = slinelist.index("stop_lon")
    count = 0
    sline = filein.readline()
    while ((count < maxfilelinecount) and (sline != '')):
        postsline = sline
        sline = sline[:-1]
        slinelist=sline.split(",")
        outset_id = slinelist[outset_id_index]
        stop_lat = float(slinelist[stop_lat_index])
        stop_lon = float(slinelist[stop_lon_index])
        if point_in_poly(stop_lat, stop_lon, geo_filter_poly):
            out_set.add(outset_id)
            fileout.write(postsline)
        count += 1
        sline = filein.readline()
    print(count, ' lines processed in ', gtfsfile)
    print(len(out_set), outsetid ,'s collected for output')

    filein.close()
    fileout.close()

    return out_set

#
# generic scan of gtfs_file by ids in in_set and create out_set of ids
#
def scan_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfsfile, maxfilelinecount, in_set, insetid, outsetid):
    print('scan ', gtfspathin+gtfsfile, ' by set of ', insetid, ' gen set of ', outsetid)
    outset_id = 'string of text'
    slinelist=[]
    out_set = set([])
    filein = open(gtfspathin+gtfsfile, 'r', encoding="utf8")
    sline = filein.readline()
    sline = sline[:-1]
    slinelist=sline.split(",")
    outset_id_index = slinelist.index(outsetid)
    inset_id_index = slinelist.index(insetid)
    count = 0
    countfoundinset = 0
    sline = filein.readline()
    while ((count < maxfilelinecount) and (sline != '')):
        sline = sline[:-1]
        slinelist=sline.split(",")
        inset_id = slinelist[inset_id_index]
        outset_id = slinelist[outset_id_index]
        if inset_id in in_set:
            out_set.add(outset_id)
            countfoundinset += 1
        count += 1
        sline = filein.readline()

    print(count, ' lines processed in ', gtfsfile)
    print(countfoundinset, ' matches of ', insetid, ' found in in_set')
    print(len(out_set), outsetid ,'s collected for output')


    filein.close()

    return out_set

#
# generic filter of gtfs_file by ids in in_set and create out_set of ids
#
def filter_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfspathout, gtfsfile, maxfilelinecount, in_set, insetid, outsetid):
    print('filter ', gtfspathin+gtfsfile, ' by set of ', insetid, ' gen set of ', outsetid)
    outset_id = 'string of text'
    slinelist=[]
    postsline = ''
    out_set = set([])
    filein = open(gtfspathin+gtfsfile, 'r', encoding="utf8")
    fileout = open(gtfspathout+gtfsfile, 'w', encoding="utf8")
    sline = filein.readline()
    fileout.write(sline)
    sline = sline[:-1]
    slinelist=sline.split(",")
    outset_id_index = slinelist.index(outsetid)
    inset_id_index = slinelist.index(insetid)
    count = 0
    countfoundinset = 0
    sline = filein.readline()
    while ((count < maxfilelinecount) and (sline != '')):
        postsline = sline
        sline = sline[:-1]
        slinelist=sline.split(",")
        inset_id = slinelist[inset_id_index]
        outset_id = slinelist[outset_id_index]
        if inset_id in in_set:
            out_set.add(outset_id)
            fileout.write(postsline)
            countfoundinset += 1
        count += 1
        sline = filein.readline()

    print(count, ' lines processed in ', gtfsfile)
    print(countfoundinset, ' matches of ', insetid, ' found in in_set')
    print(len(out_set), outsetid ,'s collected for output')


    filein.close()
    fileout.close()

    return out_set

#
# generic filter of gtfs_file by ids in in_set 
#
def filter_gtfsfile_by_in_set(gtfspathin, gtfspathout, gtfsfile, maxfilelinecount, in_set, insetid):
    print('filter ', gtfspathin+gtfsfile, ' by set of ', insetid)
    slinelist=[]
    postsline = ''
    filein = open(gtfspathin+gtfsfile, 'r', encoding="utf8")
    fileout = open(gtfspathout+gtfsfile, 'w', encoding="utf8")
    sline = filein.readline()
    fileout.write(sline)
    sline = sline[:-1]
    slinelist=sline.split(",")
    inset_id_index = slinelist.index(insetid)
    count = 0
    countfoundinset = 0
    sline = filein.readline()
    while ((count < maxfilelinecount) and (sline != '')):
        postsline = sline
        sline = sline[:-1]
        slinelist=sline.split(",")
        inset_id = slinelist[inset_id_index]
        if inset_id in in_set:
            fileout.write(postsline)
            countfoundinset += 1
        count += 1
        sline = filein.readline()

    print(count, ' lines processed in ', gtfsfile)
    print(countfoundinset, ' matches of ', insetid, ' found in in_set')


    filein.close()
    fileout.close()

    return countfoundinset
