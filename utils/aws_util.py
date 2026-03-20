import boto3
import os
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]
SQS_READ_QUEUE_NAME = os.environ["SQS_READ_QUEUE_NAME"]

S3_OBJECT_KEY_ATTR = 's3-key'

def get_aws_resources():
    s3 = boto3.client('s3')
    sqs = boto3.resource('sqs')
    try:
        queue = sqs.get_queue_by_name(QueueName=SQS_READ_QUEUE_NAME)
    except Exception as e:
        print(e)

    return s3, queue