## Site backup to S3 bucket

I'm using Scality's [cloudserver](I%27m%20using%20Scality%27s%20cloudserver%20%3Chttp://https://github.com/scality/cloudserver%3E%3E) as as replacement to AWS S3 service for development, so I don't need to worry about bucket's security from the ground up and add ACL's as needed. 
Scality provides a have a very extensive [documentation](https://s3-server.readthedocs.io/en/latest/) and also  a ready to use **docker** container that speeds up the environment deployment

Here are the steps to setup the environment:

 - **Creating the docker container that will run Scality's s3 service**
 
 This will launch the container running CloudServer at TCP port 8000:
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

