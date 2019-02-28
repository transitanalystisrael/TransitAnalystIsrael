#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# upload to AWS S3 cloud
#
import transitanalystisrael_config as cfg
import shutil
import os
import boto3
from pathlib import Path

cwd = Path.cwd()

def delete_all_objects(bucket_name):
	print('--------delete_all_objects------------')
	print(bucket_name)
	bucket2 = s3.Bucket(bucket_name)
	for obj in bucket2.objects.all():
		print(obj)
		obj.delete()

def print_objects(bucket_name):
	print('--------print_objects------------')
	print(bucket_name)
	bucket2 = s3.Bucket(bucket_name)
	for obj in bucket2.objects.all():
		print(obj.key)

#copy_to_bucket('transitanalystisrael-past', 'transitanalystisrael-backup', 'index.html')
def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
	copy_source = {
		'Bucket': bucket_from_name,
		'Key': file_name
	}
	s3.Object(bucket_to_name, file_name).copy(copy_source)

#copy_bucket('transitanalystisrael-past', 'transitanalystisrael-backup')
def copy_bucket(bucket_from_name, bucket_to_name):
	print('--------copy_bucket------------')
	print(bucket_from_name, bucket_to_name)
	bucket2 = s3.Bucket(bucket_from_name)
	for obj in bucket2.objects.all():
		print(obj.key)
		copy_to_bucket(bucket_from_name, bucket_to_name, obj.key)

def upload_localdir_to_bucket(localdir_from, bucket_to_name):
	print('--------upload_localdir_to_bucket------------')
	print(localdir_from, bucket_to_name)

#	session = boto3.Session(
#		aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
#		aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY_ID',
#		region_name='YOUR_AWS_ACCOUNT_REGION'
#	)
#	s3 = session.resource('s3')

	bucket2 = s3.Bucket(bucket_to_name)
 
	for subdir, dirs, files in os.walk(localdir_from):
		for file in files:
			full_path = os.path.join(subdir, file)
			with open(full_path, 'rb') as data:
				bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data)
				print(full_path)

def upload_localdir_w_gzip_to_bucket(localdir_from, bucket_to_name):
	print('--------upload_localdir_w_gzip_to_bucket------------')
	print(localdir_from, bucket_to_name)

	bucket2 = s3.Bucket(bucket_to_name)

	for subdir, dirs, files in os.walk(localdir_from):
		for file in files:
			full_path = os.path.join(subdir, file)
			filesize = os.path.getsize(full_path)
			print('file, filesize : ',file, filesize)
			if (file.endswith(".js") and filesize > cfg.bigjs2gzip): # skip big js files that were gziped. only the gzip file will be uploaded
				print('skipped : ',full_path)
			elif file.endswith(".gz"): # upload gzip file but remove .gz from the filename and add Metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/')[:-3], Body=data, ContentEncoding='gzip', ContentType='text/javascript')
					print('removed .gz from end : ',full_path)
			elif file.endswith(".js"): #upload small js file with metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='application/javascript')
					print('small js file : ',full_path)
			elif file.endswith(".html"): #upload with html metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='text/html')
					print('html file : ',full_path)
			elif file.endswith(".png") : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='image/png')
					print('image/png file : ',full_path)
			elif (file.endswith(".jpg") or file.endswith(".JPG")) : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='image/jpeg')
					print('image/jpg file : ',full_path)
			elif file.endswith(".css") : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='text/css')
					print('css file : ',full_path)
			else : #upload with no special treatment
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data)
					print(full_path)

#-------------------------------------------------------------------------

if cfg.get_service_date == 'auto' : 
	print('********** upload to AWS S3 cloud *************')
	current_localdir = cwd.parent / cfg.websitelocalcurrentpath
	temp_localdir = cwd.parent / cfg.temppath
	print('current_localdir : ',current_localdir)

	os.chdir(current_localdir)
	print(os.listdir(current_localdir))

	# Create an S3 resource
	s3 = boto3.resource('s3')

	# Call S3 to list current buckets
	for bucket in s3.buckets.all():
		print((bucket.name))
	#	for key in bucket.objects.all():
	#		print(key.key)

	#
	# Create an Amazon S3 Bucket - not needed - buckets are pre-created
	#
	#s3.create_bucket(Bucket='transitanalystisrael-current', CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})

	#
	# erase content of backup 
	#
	print_objects('transitanalystisrael-backup')
	delete_all_objects('transitanalystisrael-backup')

	#
	# copy content of past to backup
	#
	print_objects('transitanalystisrael-past')
	copy_bucket('transitanalystisrael-past', 'transitanalystisrael-backup')
	print_objects('transitanalystisrael-backup')

	#
	# erase content of past
	#
	print_objects('transitanalystisrael-past')
	delete_all_objects('transitanalystisrael-past')

	#
	# copy content of current to past
	#
	print_objects('transitanalystisrael-current')
	copy_bucket('transitanalystisrael-current', 'transitanalystisrael-past')
	print_objects('transitanalystisrael-past')

	#
	# erase content of current
	#
	print_objects('transitanalystisrael-current')
	delete_all_objects('transitanalystisrael-current')

	#
	# copy content of local to current
	#
	#upload_localdir_w_gzip_to_bucket(for_testing_upload_localdir, 'transitanalystisrael-current') # for testing
	upload_localdir_w_gzip_to_bucket(current_localdir, 'transitanalystisrael-current')
	print_objects('transitanalystisrael-current')

	print('------------------------------------------------------------')
	# Call S3 to list current buckets
	for bucket in s3.buckets.all():
		print((bucket.name))
	#	for key in bucket.objects.all():
	#		print(key.key)

	#
	# change current_or_past in js config file to past in transitanalystisrael-past bucket
	# this enables the TTM client to point to the correct server
	#
	# download js config file to temp dir, edit file, then upload
	#download
	s3.Bucket('transitanalystisrael-past').download_file('docs/transitanalystisrael_config.js', temp_localdir / 'transitanalystisrael_config.js')
	#edit
	jsfile = 'transitanalystisrael_config.js'
	tempjsfile = 'temp_config.js'
	in_dir = temp_localdir
	out_dir = temp_localdir
	maxfilelinecount = 2000
	print('input from ', in_dir / jsfile)
	print('output to ', out_dir / tempjsfile)
	filein = open(in_dir / jsfile, 'r', encoding="utf8")
	fileout = open(out_dir / tempjsfile, 'w', encoding="utf8")
	count = 0
	sline = filein.readline()
	while ((count < maxfilelinecount) and (sline != '')):
		if sline.find('var cfg_current_or_past') == 0 : 
			postsline = sline.replace("'current'","'past'")
			fileout.write(postsline)
		else :
			postsline = sline
			fileout.write(postsline)
		#print len(sline), sline
		count +=1
		sline = filein.readline()
	print('------------------')
	print(' infile line count ',count)
	filein.close()
	fileout.close()
	print('closed ', in_dir / jsfile)
	print('closed ', out_dir / tempjsfile)
	shutil.copyfile(out_dir / tempjsfile,out_dir / jsfile)
	os.remove(out_dir / tempjsfile)
	#upload
	with open(out_dir / jsfile, 'rb') as data:
		s3.Bucket('transitanalystisrael-past').put_object(Key='docs/transitanalystisrael_config.js', Body=data, ContentType='application/javascript')
		print('uploaded : ', out_dir / jsfile)
#---------------------------------------------------------------------------------------
else : # cfg.get_service_date == 'on_demand'
	on_demand_dir = cwd.parent / cfg.websitelocalondemandpath.replace('yyyymmdd', cfg.gtfsdate)
	print('********** upload to AWS S3 cloud *************')
	on_demand_localdir = on_demand_dir
	temp_localdir = cwd.parent / cfg.temppath
	print('on_demand_localdir : ',on_demand_localdir)

	os.chdir(on_demand_localdir)
	print(os.listdir(on_demand_localdir))

	# Create an S3 resource
	s3 = boto3.resource('s3')

	# Call S3 to list current buckets
	for bucket in s3.buckets.all():
		print((bucket.name))
	#	for key in bucket.objects.all():
	#		print(key.key)

	#
	# Create an Amazon S3 Bucket - needed for on demand. for auto - buckets are pre-created
	#
	on_demand_bucket = 'transitanalystisrael-'+cfg.gtfsdate
	s3.create_bucket(Bucket=on_demand_bucket, CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})

	#
	# copy content of local to on_demand bucket
	#
	#upload_localdir_w_gzip_to_bucket(for_testing_upload_localdir, 'transitanalystisrael-current') # for testing
	upload_localdir_w_gzip_to_bucket(on_demand_localdir, on_demand_bucket)
	print_objects(on_demand_bucket)

	print('------------------------------------------------------------')
	# Call S3 to list current buckets
	for bucket in s3.buckets.all():
		print((bucket.name))
	#	for key in bucket.objects.all():
	#		print(key.key)

