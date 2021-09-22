## S3 Object Storage playground

This repository provides instructions and examples for using Amazon's Simple Storage Service to store and manage data through different methods.

I'm using Scality's [cloudserver](https://github.com/scality/cloudserver) as as replacement to AWS S3 service for development, so I don't need to worry about bucket's security from the ground up and add ACL's as needed.

Scality provides a have a very extensive [documentation](https://s3-server.readthedocs.io/en/latest/) and also  a ready to use **docker** container that speeds up the environment deployment

Here are the steps to setup the environment:

- **Creating the docker container that will run Scality's s3 service**

This will launch the container running CloudServer at TCP port 8000:<p></p>

``docker run -d --name s3server -p 8000:8000 scality/s3server``

  - **Install AWS boto3 library**

 Connection with the local s3 server can be done through regular AWS boto3 Python library. For testing purposes I'm using python since it's the simplest language available for the task

``pip3 install boto3``

  

- **Using boto3 to connect into ClousServer s3 service**

Boto3 connection setup to the local s3 service requires the ``endpoint`` definition:

  

<pre><code>import boto3
bucket_name="mytestbucket"
session = boto3.session.Session()

s3_client = session.client(
	service_name='s3',
	aws_access_key_id='accessKey1',
	aws_secret_access_key='verySecretKey1',
	endpoint_url='http://localhost:8000',</code></pre>

  - **Listing existing groups**
<pre><code>import json
print(json.dumps(s3_client.list_buckets(),indent=4,default=str))
</code></pre>

- **Creating a new bucket**
<pre><code>bucket_name="mytestbucket"
s3_client.create_bucket(ACL='public-read-write',Bucket=bucket_name)
</code></pre>

- **Uploading file to a bucket as an object**
<pre><code>bucketName="mytestbucket"
localFile="/directory/myFile.txt"
objectKey="myFile.txt"
s3_client.put_object(
	ACL='public-read',
	Body=localFile,
	Bucket=bucketName,
	Key=objectKey,
	)</code></pre>

- **Multi-part upload files**

First I downloaded a the [Big Buck Bunny video file](http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4) which is provided freely by the Blender team:

``wget http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4``

The code below is based on this [medium article](https://medium.com/analytics-vidhya/aws-s3-multipart-upload-download-using-boto3-python-sdk-2dedb0945f11). It uses a nice Callback to ProgressPercentage function which shows the upload progress:

<pre><code>import os, threading, sys
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
			sys.stdout.write(
				"\r%s  %s / %s  (%.2f%%)" % (
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
		Callback=ProgressPercentage(localFilename))</code></pre>



- **Using the aws-cli to access the buckets**

This service doesn't implement the ListObjectV2 method, so it's necessary to install this specific AWS CLI version:
<pre><code>pip install awscli==1.16.14</code></pre>

Next. create the aws configuration file and add the user key and secret:
<pre><code>mkdir ~/.aws
echo "[default]" | tee ~/.aws/config
echo "[default]
aws_access_key_id = accessKey1
aws_secret_access_key = verySecretKey1" | tee  ~/.aws/credentials</code></pre>

After that the aws s3 commands can be issued as usual:

<pre><code>$ aws s3 ls s3://mytestbucket --endpoint=http://localhost:8000

2021-09-21 18:37:48  158008374 BigBuckBunny.mp4</code></pre>
