#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# upload ondemand to AWS S3 cloud
# the ondemand date bucket is created in S3 before the local dir is copied to the bucket
#
import transitanalystisrael_config as cfg
import shutil
import os
import boto3
import json
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

def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
	copy_source = {
		'Bucket': bucket_from_name,
		'Key': file_name
	}
	s3.Object(bucket_to_name, file_name).copy(copy_source)

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
			if (file.endswith(".js") and filesize > int(cfg.bigjs2gzip) and not subdir.endswith("dist")): # skip big js files that were gziped. only the gzip file will be uploaded. does not apply to dist dir that does not go through gzip.
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
			elif (file.endswith(".ico") or file.endswith(".ICO")) : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='image/x-icon')
					print('image/ico file : ',full_path)
			elif file.endswith(".css") : #upload with image metadata
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='text/css')
					print('css file : ',full_path)
			else : #upload with no special treatment
				with open(full_path, 'rb') as data:
					bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data)
					print(full_path)

#-------------------------------------------------------------------------

print('********** upload ondemand to AWS S3 cloud *************')
ondemand_localdir = cwd.parent / cfg.websitelocalondemandpath.replace('yyyymmdd', cfg.gtfsdate)
print('ondemand_localdir : ',ondemand_localdir)

os.chdir(ondemand_localdir)
print(os.listdir(ondemand_localdir))

# Create an S3 resource
s3 = boto3.resource('s3')

# Call S3 to list current buckets
for bucket in s3.buckets.all():
	print((bucket.name))
#	for key in bucket.objects.all():
#		print(key.key)

#
# Create an Amazon S3 Bucket 
#
on_demand_bucket = cfg.bucket_prefix+cfg.gtfsdate
s3.create_bucket(Bucket=on_demand_bucket, CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})

# Create the configuration for the website
website_configuration = {'ErrorDocument': {'Key': 'error.html'}, 'IndexDocument': {'Suffix': 'index.html'},}
# Set the new policy on the selected bucket
s3c.put_bucket_website(Bucket=on_demand_bucket, WebsiteConfiguration=website_configuration)

# Create the bucket policy
bucket_policy = {
	'Version': '2012-10-17',
	'Statement': [{
		'Sid': 'PublicReadGetObject',
		'Effect': 'Allow',
		'Principal': '*',
		'Action': ['s3:GetObject'],
		'Resource': "arn:aws:s3:::%s/*" % on_demand_bucket
	}]
}
# Convert the policy to a JSON string
bucket_policy = json.dumps(bucket_policy)
# Set the new policy on the given bucket
s3c.put_bucket_policy(Bucket=on_demand_bucket, Policy=bucket_policy)

#
# copy content of local to ondemand
#
#upload_localdir_w_gzip_to_bucket(for_testing_upload_localdir, cfg.bucket_prefix+cfg.gtfsdate) # for testing
upload_localdir_w_gzip_to_bucket(ondemand_localdir, cfg.bucket_prefix+cfg.gtfsdate)
print_objects(cfg.bucket_prefix+cfg.gtfsdate)

print('------------------------------------------------------------')
# Call S3 to list current buckets
for bucket in s3.buckets.all():
	print((bucket.name))
#	for key in bucket.objects.all():
#		print(key.key)

