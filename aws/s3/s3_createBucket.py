#!/usr/bin/env python3
import boto3
import json

bucket_name="mytestbucket"

session = boto3.session.Session()

s3_client = session.client(
    service_name='s3',
    aws_access_key_id='accessKey1',
    aws_secret_access_key='verySecretKey1',
    endpoint_url='http://localhost:8000',
)
result=s3_client.create_bucket(ACL='public-read-write',Bucket=bucket_name)
print(json.dumps(result,indent=4,default=str))
