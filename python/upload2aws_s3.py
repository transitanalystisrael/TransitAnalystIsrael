#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# upload to AWS S3 cloud
#
import transitanalystisrael_config as cfg
import shutil
import os
import boto3

print '********** upload to AWS S3 cloud *************'
current_localdir = cfg.websitelocalpath[:-1]+'_current'
past_localdir = cfg.websitelocalpath[:-1]+'_past'
no_data_localdir = cfg.websitelocalpath[:-1]+'_no_data'
for_testing_upload_localdir = cfg.websitelocalpath[:-1]+'_for_testing_upload'
print 'current_localdir : ',current_localdir
print 'past_localdir : ',past_localdir
print 'no_data_localdir : ',no_data_localdir
print 'for_testing_upload_localdir : ',for_testing_upload_localdir
os.chdir(current_localdir)
print os.listdir(current_localdir)

def delete_all_objects(bucket_name):
	print '--------delete_all_objects------------'
	print bucket_name
	bucket2 = s3.Bucket(bucket_name)
	for obj in bucket2.objects.all():
		print obj
		obj.delete()

def print_objects(bucket_name):
	print '--------print_objects------------'
	print bucket_name
	bucket2 = s3.Bucket(bucket_name)
	for obj in bucket2.objects.all():
		print obj.key

#copy_to_bucket('transitanalystisrael-past', 'transitanalystisrael-backup', 'index.html')
def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
	copy_source = {
		'Bucket': bucket_from_name,
		'Key': file_name
	}
	s3.Object(bucket_to_name, file_name).copy(copy_source)

#copy_bucket('transitanalystisrael-past', 'transitanalystisrael-backup')
def copy_bucket(bucket_from_name, bucket_to_name):
	print '--------copy_bucket------------'
	print bucket_from_name, bucket_to_name
	bucket2 = s3.Bucket(bucket_from_name)
	for obj in bucket2.objects.all():
		print obj.key
		copy_to_bucket(bucket_from_name, bucket_to_name, obj.key)

def upload_localdir_to_bucket(localdir_from, bucket_to_name):
	print '--------upload_localdir_to_bucket------------'
	print localdir_from, bucket_to_name

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
				bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/'), Body=data)
				print full_path

def upload_localdir_w_gzip_to_bucket(localdir_from, bucket_to_name):
	print '--------upload_localdir_w_gzip_to_bucket------------'
	print localdir_from, bucket_to_name

	bucket2 = s3.Bucket(bucket_to_name)

	for subdir, dirs, files in os.walk(localdir_from):
		for file in files:
			full_path = os.path.join(subdir, file)
			filesize = os.path.getsize(full_path)
			print 'file, filesize : ',file, filesize
			if (file.endswith(".js") and filesize > cfg.bigjs2gzip): # skip big js files that were gziped. only the gzip file will be uploaded
				print 'skipped : ',full_path
			elif file.endswith(".gz"): # upload gzip file but remove .gz from the filename and add Metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/')[:-3], Body=data, ContentEncoding='gzip', ContentType='text/javascript')
					print 'removed .gz from end : ',full_path
			elif file.endswith(".js"): #upload small js file with metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/'), Body=data, ContentType='application/javascript')
					print 'small js file : ',full_path
			elif file.endswith(".html"): #upload with html metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/'), Body=data, ContentType='text/html')
					print 'html file : ',full_path
			elif file.endswith(".png") : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/'), Body=data, ContentType='image/png')
					print 'image/png file : ',full_path
			elif (file.endswith(".jpg") or file.endswith(".JPG")) : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/'), Body=data, ContentType='image/jpeg')
					print 'image/jpg file : ',full_path
			elif file.endswith(".css") : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/'), Body=data, ContentType='text/css')
					print 'css file : ',full_path
			else : #upload with no special treatment
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(localdir_from)+1:].replace('\\','/'), Body=data)
					print full_path

#-------------------------------------------------------------------------

# Create an S3 resource
s3 = boto3.resource('s3')

# Call S3 to list current buckets
for bucket in s3.buckets.all():
	print(bucket.name)
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

'''
toolslist = ['lines_on_street', 'line_freq', 'muni_fairsharescore', 'muni_score_lists_and_charts', 'muni_tpd_per_line', 'muni_transitscore', 'stops_near_trainstops_editor', 'tpd_at_stops_per_line', 'tpd_near_trainstops_per_line', 'transitscore']
for tooldir in toolslist:
	print '# ',tooldir
	tooldirfilelist = os.listdir(current_localdir+tooldir)
	for filename in tooldirfilelist :
		print filename
		filepath = current_localdir+tooldir+'\\'+filename
		filesize = os.path.getsize(filepath)
		if (filename.endswith(".js") and filesize <= cfg.bigjssize2gzip) or (filename.endswith(".html") or filename.endswith(".png")):
			print '  ',filepath, filesize
		elif filename.endswith(".gz") :
			print '  GZIP-> ',filepath, filesize
'''

print '------------------------------------------------------------'
# Call S3 to list current buckets
for bucket in s3.buckets.all():
	print(bucket.name)
#	for key in bucket.objects.all():
#		print(key.key)

