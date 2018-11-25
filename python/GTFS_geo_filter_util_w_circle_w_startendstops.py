#!/usr/bin/env python
#--------------------------------------------------
# filter the GTFS files by a given area
#
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
## Call the function with the points and the polygon
# print point_in_poly(point_x,point_y,polygon

# Determine if a point (lat, lon) is inside a given circle or not
# Circle is center location and radius: c_lat, c_lon, r. r is in meters
# This function returns True or False. 

from geopy.distance import vincenty

def point_in_cicle(lat,lon,c_lat,c_lon,r):
	inside = False
	loc = (lat, lon)
	c_loc = (c_lat, c_lon)
	distance = vincenty(loc,c_loc).m
	if distance <= r : 
		inside = True
	return inside



#
# collect out set of stop ids from stops.txt of stops inside geo_filter circle and write lines of inside stops to stops.txt file out
#
def scan_stops_by_circle(gtfspathin, gtfspathout, maxfilelinecount, c_lat, c_lon, r):
    gtfsfile = 'stops.txt'
    outsetid = 'stop_id'
    outset_id = 'string of text'
    stop_lat = 0.0
    stop_lon = 0.0
    slinelist=[]
    postsline = ''
    print 'scan_stops_by_circle'
    print gtfspathin+gtfsfile
    out_set = set([])
    filein = open(gtfspathin+gtfsfile, 'r')
    fileout = open(gtfspathout+gtfsfile, 'w')
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
        if point_in_cicle(stop_lat, stop_lon, float(c_lat), float(c_lon), float(r)):
            out_set.add(outset_id)
            fileout.write(postsline)
        count += 1
        sline = filein.readline()
    print count, ' lines processed in ', gtfsfile
    print len(out_set), outsetid ,'s collected for output'

    filein.close()
    fileout.close()

    return out_set

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
    print 'scan_stops_by_lat_lon'
    print gtfspathin+gtfsfile
    out_set = set([])
    filein = open(gtfspathin+gtfsfile, 'r')
    fileout = open(gtfspathout+gtfsfile, 'w')
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
    print count, ' lines processed in ', gtfsfile
    print len(out_set), outsetid ,'s collected for output'

    filein.close()
    fileout.close()

    return out_set

#
# collect set of trips from stop_times.txt where both start stop and end stop of trip are in given set of stops
#
import csv
def collect_trips_w_startandend_stops_in_stop_set(gtfspathin, stop_set):
	print 'scan ', gtfspathin+'stop_times.txt by set of stops to gen set of trips where both start stop and end stop of trip are in given set of stops'
	gtfsfile = 'stop_times.txt'
	trip_set = set([])
	txtfilein = gtfspathin+gtfsfile
	trips_dict = {} # trip_id: [first_stop_sequence, first_stop_id, end_stop_sequence, end_stop_id]
	with open(txtfilein, 'rb') as f:
		reader = csv.reader(f)
		header = reader.next() # [trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled]
		print header
		for row in reader:
			#print row
			trip_id = row[0]
			stop_id = row[3]
			stop_sequence = row[4]
			if trip_id in trips_dict : # update as needed to find first and end stop
				if (int(trips_dict[trip_id][0]) > int(stop_sequence)) : #new sequence number is smaller than first
					lowest_sequence = stop_sequence
					lowest_stop_id = stop_id
				else :
					lowest_sequence = trips_dict[trip_id][0]
					lowest_stop_id = trips_dict[trip_id][1]
				if (int(trips_dict[trip_id][2]) < int(stop_sequence)) : #new sequence number is bigger than last
					highest_sequence = stop_sequence
					highest_stop_id = stop_id
				else :
					highest_sequence = trips_dict[trip_id][2]
					highest_stop_id = trips_dict[trip_id][3]
				trips_dict[trip_id] = [lowest_sequence, lowest_stop_id, highest_sequence, highest_stop_id]
			else : # not in dict then add
				trips_dict[trip_id] = [stop_sequence, stop_id, stop_sequence, stop_id]
				if len(trips_dict)%10000 == 0 : print len(trips_dict)

	print trip_id, trips_dict[trip_id] #print last
	print 'trips_dict loaded. trip count ', len(trips_dict)
	
	for trip_id, [first_stop_sequence, first_stop_id, end_stop_sequence, end_stop_id], in trips_dict.iteritems() :
		if first_stop_sequence != '1' : 	# verify trips_dict lowest sequence is "1" for all trips
			print '********** error ********* lowest sequence is not "1" ', trip_id, trips_dict[trip_id]
		else :
			if (first_stop_id in stop_set) and (end_stop_id in stop_set) :
				trip_set.add(trip_id)
				print 'added trip_id : ', trip_id
	print 'trip_id count collected with first and last stop in stop set : ', len(trip_set)
	return trip_set

#
# generic scan of gtfs_file by ids in in_set and create out_set of ids
#
def scan_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfsfile, maxfilelinecount, in_set, insetid, outsetid):
    print 'scan ', gtfspathin+gtfsfile, ' by set of ', insetid, ' gen set of ', outsetid
    outset_id = 'string of text'
    slinelist=[]
    out_set = set([])
    filein = open(gtfspathin+gtfsfile, 'r')
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

    print count, ' lines processed in ', gtfsfile
    print countfoundinset, ' matches of ', insetid, ' found in in_set'
    print len(out_set), outsetid ,'s collected for output'


    filein.close()

    return out_set

#
# generic filter of gtfs_file by ids in in_set and create out_set of ids
#
def filter_gtfsfile_by_in_set_gen_out_set(gtfspathin, gtfspathout, gtfsfile, maxfilelinecount, in_set, insetid, outsetid):
    print 'filter ', gtfspathin+gtfsfile, ' by set of ', insetid, ' gen set of ', outsetid
    outset_id = 'string of text'
    slinelist=[]
    postsline = ''
    out_set = set([])
    filein = open(gtfspathin+gtfsfile, 'r')
    fileout = open(gtfspathout+gtfsfile, 'w')
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

    print count, ' lines processed in ', gtfsfile
    print countfoundinset, ' matches of ', insetid, ' found in in_set'
    print len(out_set), outsetid ,'s collected for output'


    filein.close()
    fileout.close()

    return out_set

#
# generic filter of gtfs_file by ids in in_set 
#
def filter_gtfsfile_by_in_set(gtfspathin, gtfspathout, gtfsfile, maxfilelinecount, in_set, insetid):
    print 'filter ', gtfspathin+gtfsfile, ' by set of ', insetid
    slinelist=[]
    postsline = ''
    filein = open(gtfspathin+gtfsfile, 'r')
    fileout = open(gtfspathout+gtfsfile, 'w')
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

    print count, ' lines processed in ', gtfsfile
    print countfoundinset, ' matches of ', insetid, ' found in in_set'


    filein.close()
    fileout.close()

    return countfoundinset
