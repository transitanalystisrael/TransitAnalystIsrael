#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# test upload to AWS S3 cloud
#
import transitanalystisrael_config as cfg
import shutil
import os
import boto3
import json
from pathlib import Path

cwd = Path.cwd()
current_localdir = cwd.parent / cfg.websitelocalcurrentpath

def upload_localdir_w_gzip_to_bucket(localdir_from, bucket_to_name):
	print('--------upload_localdir_w_gzip_to_bucket------------')
	print(localdir_from, bucket_to_name)

	#bucket2 = s3.Bucket(bucket_to_name)

	for subdir, dirs, files in os.walk(localdir_from):
		for file in files:
			full_path = os.path.join(subdir, file)
			filesize = os.path.getsize(full_path)
			print('subdir, file, filesize : ', subdir, file, filesize)
			if (file.endswith(".js") and filesize > int(cfg.bigjs2gzip) and not subdir.endswith("dist")): # skip big js files that were gziped. only the gzip file will be uploaded
				print('skipped : ',full_path)
			elif file.endswith(".gz"): # upload gzip file but remove .gz from the filename and add Metadata
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/')[:-3], Body=data, ContentEncoding='gzip', ContentType='text/javascript')
					print('removed .gz from end : ',full_path)
			elif file.endswith(".js"): #upload small js file with metadata
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='application/javascript')
					print('small js file : ',full_path)
			elif file.endswith(".html"): #upload with html metadata
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='text/html')
					print('html file : ',full_path)
			elif file.endswith(".png") : #upload with image metadata
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='image/png')
					print('image/png file : ',full_path)
			elif (file.endswith(".jpg") or file.endswith(".JPG")) : #upload with image metadata
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='image/jpeg')
					print('image/jpg file : ',full_path)
			elif (file.endswith(".ico") or file.endswith(".ICO")) : #upload with image metadata
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='image/x-icon')
					print('image/ico file : ',full_path)
			elif file.endswith(".css") : #upload with image metadata
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data, ContentType='text/css')
					print('css file : ',full_path)
			else : #upload with no special treatment
				with open(full_path, 'rb') as data:
					#bucket2.put_object(Key=full_path[len(str(localdir_from))+1:].replace('\\','/'), Body=data)
					print(full_path)

upload_localdir_w_gzip_to_bucket(current_localdir, 'transitanalystisrael-testing123')