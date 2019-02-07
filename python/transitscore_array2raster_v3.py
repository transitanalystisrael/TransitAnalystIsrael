#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# convert transitscore txt grid file - transit_score_israelyyyymmdd.txt - to an array of transitscore from 1-100 
# then convert the array to a raster
# output ts_rendered _israelyyyymmdd.png
#
print '----------------- generate raster from grid file--------------------------'
print 'convert transitscore txt grid file - transit_score_all_israel.txt - to an array of transitscore from 1-100  '
print ' then convert the array to a raster'
print 'output ts_rendered _israelyyyymmdd.png'
#---------------------------------------------------------------------------------------------------
# array2raster with gdal from - https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
#
from osgeo import gdal
import ogr, os, osr
import numpy as np
import struct
import time
import csv
#
print "Local current time :", time.asctime( time.localtime(time.time()) )
#
def main(gtfsdate, gtfsdirbase, processedpath):
	parent_path = processedpath
	gtfsdir = gtfsdirbase+gtfsdate
	tsfilein = 'transit_score_'+gtfsdir+'.txt'
	tsfileout = 'ts_unproj.tif'

	ilminlat = 29.490000 # Israel min lat
	ilminlon = 34.280000 # Israel min lon

	lat100 = 0.0011100 # grid step of 100m
	lon100 = 0.0009600 # grid step of 100m

	#
	# load file
	#
	# >>> load transitscore file
	transitscore_list = []
	max_grid_lat = 0
	max_grid_lon = 0
	maxts = 0
	with open(parent_path+tsfilein, 'rb') as ts_f:
		readerts = csv.reader(ts_f)
		headerts = readerts.next()
		print headerts
		for row in readerts:
			#print row
			grid_lat = int(row[0])
			grid_lon = int(row[1])
			ts = int(row[2])
			max_grid_lat = max(max_grid_lat, grid_lat)
			max_grid_lon = max(max_grid_lon, grid_lon)
			maxts = max(maxts, ts)
			transitscore_list.append([grid_lat, grid_lon, ts])
	#print transitscore_list
	print 'transitscore_list loaded. ts count ', len(transitscore_list)
	print 'max_grid_lat, max_grid_lon : ', max_grid_lat, max_grid_lon
	print 'max_lat, max_lon : ', ilminlat+(1+max_grid_lat)*lat100, ilminlon+(1+max_grid_lon)*lon100
	print 'maxts:', maxts

	n = max_grid_lat+1
	m = max_grid_lon+1
	ts_grid = [0] * n
	for i in range(n):
		ts_grid[i] = [0] * m

	for [grid_lat, grid_lon, ts] in transitscore_list :
		ts_grid[grid_lat][grid_lon] = ts

	#print ts_grid[:4][:4]

	#---------------------------------------------------------------------------------------------
	# convert array to raster and output file ts.tif 
	#
	max_lat = ilminlat+(1+max_grid_lat)*lat100
	xsize = lon100
	ysize = -lat100

	newRasterfn = parent_path+tsfileout
	array = np.array(ts_grid)
	print 'converting array - '
	print 'newRasterfn,len(ts_grid),len(ts_grid[1]) : ',newRasterfn,len(ts_grid),len(ts_grid[1])

	reversed_arr = array[::-1] # reverse array so the tif looks like the array

	cols = reversed_arr.shape[1]
	rows = reversed_arr.shape[0]
	originX = ilminlon
	originY = max_lat

	driver = gdal.GetDriverByName('GTiff')
	outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte) # default GDT_Byte
	geotransform = (originX, xsize, 0, originY, 0, ysize)
	outRaster.SetGeoTransform(geotransform)
	outband = outRaster.GetRasterBand(1)
	outband.WriteArray(reversed_arr)
	outRasterSRS = osr.SpatialReference()
	outRasterSRS.SetWellKnownGeogCS('WGS84')
	#outRasterSRS.ImportFromEPSG(4326)
	geoproj = outRasterSRS.ExportToWkt()
	outRaster.SetProjection(geoproj)
	outband.FlushCache()
	outRaster = None

	print 'geotransform, geoproj, xsize, ysize :'
	print geotransform
	print geoproj
	print xsize, ysize 
	print ("Saving file: " + parent_path+tsfileout + " ...")
	print ("Saved file: " + tsfileout)

	#------------------------------------------------------------------
	# get some info on file created ts_unproj.tif 
	import sys
	print '----------------------------------os.system("gdalinfo ts_unproj.tif ")'
	#os.system("gdalinfo ts_unproj.tif ")
	#------------------------------------------------------------------------
	# translate in order to scale back to 0-100
	old_ds = gdal.Open('ts_unproj.tif')
	if old_ds is None:
		print 'Unable to open INPUT.tif'
		sys.exit(1)

	print "[ RASTER BAND COUNT old_ds]: ", old_ds.RasterCount
	for band in range( old_ds.RasterCount ):
		band += 1
		print "[ GETTING BAND ]: ", band
		srcband = old_ds.GetRasterBand(band)
		if srcband is None:
			continue

		stats = srcband.GetStatistics( True, True )
		if stats is None:
			continue

		print "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
					stats[0], stats[1], stats[2], stats[3] )
	minvalue = str(int(stats[0]))
	maxvalue = str(int(stats[1]))
	old_ds = None

	print '----------------------------------os.system("gdal_translate ts_unproj.tif ts_scaled.tif -scale 0 88 0 100")'
	os.system("gdal_translate ts_unproj.tif ts_scaled.tif -scale "+minvalue+" "+maxvalue+" 0 100") #  scale 

	#----------------------------------------------------------------------------
	# project ts_scaled.tif to 3857 and create ts.tif
	srs = osr.SpatialReference()
	#srs.SetWellKnownGeogCS('WGS84') # from sample in book
	srs.ImportFromEPSG(3857)
	old_ds = gdal.Open('ts_scaled.tif')
	if old_ds is None:
		print 'Unable to open INPUT.tif'
		sys.exit(1)

	print "[ RASTER BAND COUNT old_ds]: ", old_ds.RasterCount
	for band in range( old_ds.RasterCount ):
		band += 1
		print "[ GETTING BAND ]: ", band
		srcband = old_ds.GetRasterBand(band)
		if srcband is None:
			continue

		stats = srcband.GetStatistics( True, True )
		if stats is None:
			continue

		print "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
					stats[0], stats[1], stats[2], stats[3] )

	vrt_ds = gdal.AutoCreateWarpedVRT(old_ds, None, srs.ExportToWkt(), gdal.GRA_Bilinear)
	#vrt_ds = gdal.AutoCreateWarpedVRT(old_ds, None, srs.ExportToWkt(), gdal.GRA_NearestNeighbour)

	print "[ RASTER BAND COUNT vrt_ds]: ", vrt_ds.RasterCount
	for band in range( vrt_ds.RasterCount ):
		band += 1
		print "[ GETTING BAND ]: ", band
		srcband = vrt_ds.GetRasterBand(band)
		if srcband is None:
			continue

		stats = srcband.GetStatistics( True, True )
		if stats is None:
			continue

		print "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
					stats[0], stats[1], stats[2], stats[3] )


	dst_ds = gdal.GetDriverByName('GTiff').CreateCopy('ts.tif', vrt_ds)
	#Properly close the datasets to flush to disk
	old_ds = None
	vrt_ds = None
	dst_ds = None

	print '----------------------------------os.system("gdalinfo ts.tif ")'
	#os.system("gdalinfo ts.tif ")

	#---------------------------------------------------------------------------
	# use GDAL CreateCopy to convert ts.tif >>> to >>> ts.png
	#
	print 'use GDAL CreateCopy to convert ts.tif >>> to >>> ts.png'

	#Open existing dataset
	src_ds = gdal.Open( "ts.tif" )
	if src_ds is None:
		print 'Unable to open INPUT.tif'
		sys.exit(1)

	#Open output format driver, see gdal_translate --formats for list
	format = "PNG"
	driver = gdal.GetDriverByName( format )

	#Output to new format
	dst_ds = driver.CreateCopy( "ts.png", src_ds, 0 )
	print dst_ds.GetMetadata()

	#Properly close the datasets to flush to disk
	src_ds = None
	dst_ds = None

	print '----------------------------------os.system("gdalinfo ts.png")'
	#os.system("gdalinfo ts.png")

	#---------------------------------------------------------------------------
	# use GDAL gdaldem to convert ts.tif >>> to >>> ts_rendered.tif
	#
	print 'use GDAL gdaldem to convert ts.tif >>> to >>> ts_rendered.tif'

	os.system("gdaldem color-relief ts.tif rgb_color.txt ts_rendered.tif")
	print '----------------------------------os.system("gdalinfo ts_rendered.tif")'
	#os.system("gdalinfo ts_rendered.tif")

	#---------------------------------------------------------------------------
	# use GDAL CreateCopy to convert ts_rendered.tif >>> to >>> ts_rendered.png
	#
	print 'use GDAL CreateCopy to convert ts_rendered.tif >>> to >>> ts_rendered.png'

	#Open existing dataset
	src_ds = gdal.Open( "ts_rendered.tif" )
	if src_ds is None:
		print 'Unable to open INPUT.tif'
		sys.exit(1)

	#Open output format driver, see gdal_translate --formats for list
	format = "PNG"
	driver = gdal.GetDriverByName( format )

	#Output to new format
	dst_ds = driver.CreateCopy( 'ts_rendered_'+gtfsdir+'.png', src_ds, 0 )

	#Properly close the datasets to flush to disk
	dst_ds = None
	src_ds = None

	print '----------------------------------os.system("gdalinfo ts_rendered.png")'
	os.system('gdalinfo ts_rendered_'+gtfsdir+'.png')

	print 'done'
