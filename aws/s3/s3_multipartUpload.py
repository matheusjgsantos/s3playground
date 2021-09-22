#!/usr/bin/env python3
#The code below is based on this [medium article](https://medium.com/analytics-vidhya/aws-s3-multipart-upload-download-using-boto3-python-sdk-2dedb0945f11). It uses a nice Callback to ProgressPercentage function which shows the upload progress:

import os, threading, sys
import boto3
import json
from boto3.s3.transfer import TransferConfig

config = TransferConfig(
	multipart_threshold=1024 * 25,
	max_concurrency=10,
	multipart_chunksize=1024 * 25,
	use_threads=True
	)
 
bucketName="mytestbucket"
localFilename="BigBuckBunny.mp4"
keyName="BigBuckBunny.mp4"

class  ProgressPercentage(object):
	def  __init__(self, filename):
		self._filename = filename
		self._size = float(os.path.getsize(filename))
		self._seen_so_far = 0
		self._lock = threading.Lock()

	def  __call__(self, bytes_amount):
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write( "\r%s  %s / %s  (%.2f%%)" % (
				self._filename, self._seen_so_far, self._size,
				percentage))
			sys.stdout.flush()

session = boto3.session.Session()
s3_resource = session.resource(
	service_name='s3',
	aws_access_key_id='accessKey1',
	aws_secret_access_key='verySecretKey1',
	endpoint_url='http://localhost:8000',
)

s3_resource.Object(bucketName, keyName).upload_file(localFilename,ExtraArgs={'ContentType': 'video/mp4'},
		Config=config,
		Callback=ProgressPercentage(localFilename))
