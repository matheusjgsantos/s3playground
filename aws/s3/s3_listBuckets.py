#!/usr/bin/env python3
import boto3
import json

session = boto3.session.Session()

s3_client = session.client(
    service_name='s3',
    aws_access_key_id='accessKey1',
    aws_secret_access_key='verySecretKey1',
    endpoint_url='http://localhost:8000',
)

print(json.dumps(s3_client.list_buckets(),indent=4,default=str))
