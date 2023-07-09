import boto3

def copy_object(source_bucket, source_key, destination_bucket, destination_key):
    s3_client = boto3.client("s3")
    s3_client.copy_object(
        Bucket=destination_bucket,
        Key=destination_key,
        CopySource={"Bucket": source_bucket, "Key": source_key},
    )

def delete_object(bucket, key):
    s3_client = boto3.client("s3")
    s3_client.delete_object(Bucket=bucket, Key=key)

def encrypt_object(bucket, key, algorithm):
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=bucket, Key=key, ServerSideEncryption=algorithm)
