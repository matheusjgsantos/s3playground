## Site backup to S3 bucket

**Create the docker container that will run Scality's s3 service**
``docker run -d --name s3server -p 8000:8000 scality/s3server``

**Installing boto3 library**
Connection with the local s3 server can be done through regular AWS boto3 library.
``pip3 install boto3``

**Using boto3 to connect into Scality s3 service**
Boto3 connection setup to the local s3 service requires the ``endpoint`` definition:

<pre><code>import boto3
bucket_name="mytestbucket"
session = boto3.session.Session()

s3_client = session.client(

service_name='s3',
	aws_access_key_id='accessKey1',
	aws_secret_access_key='verySecretKey1',
	endpoint_url='http://localhost:8000',</code></pre>

**Listing existing groups**
<pre><code>import json
print(json.dumps(s3_client.list_buckets(),indent=4,default=str))
</code></pre>

**Creating a new bucket**
<pre><code>bucket_name="mytestbucket"
s3_client.create_bucket(ACL='public-read-write',Bucket=bucket_name)
</code></pre>

**Uoloading file to a bucket as an object**
<pre><code>bucketName="mytestbucket"
localFile="/directory/myFile.txt"
objectKey="myFile.txt"
s3_client.put_object(
	ACL='public-read',
	Body=localFile,
	Bucket=bucketName,
	Key=objectKey,
)</code></pre>

