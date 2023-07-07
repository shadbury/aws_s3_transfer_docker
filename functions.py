import os
import time
import logging
import boto3
from botocore.exceptions import NoCredentialsError
import traceback
import progressbar
from tkinter import messagebox



def setup_logging():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='transfer.log', level=logging.INFO, format=log_format)


def delete_file(client, bucket, key):
    client.delete_object(Bucket=bucket, Key=key)


def list_buckets(profile):
    session = boto3.Session(profile_name=profile)
    client = session.client('s3')
    response = client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return buckets


def get_bucket_encryption(client, bucket):
    response = client.get_bucket_encryption(Bucket=bucket)
    return response


def encrypt_bucket(client, bucket, checksum, algorithm, kmsmasterkeyid, bucketKeyEnabled):
    if kmsmasterkeyid:
        client.put_bucket_encryption(
            Bucket=bucket,
            ChecksumAlgorithm=checksum,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': algorithm,
                            'KMSMasterKeyID': kmsmasterkeyid
                        },
                        'BucketKeyEnabled': bucketKeyEnabled
                    },
                ]
            }
        )
    else:
        client.put_bucket_encryption(
            Bucket=bucket,
            ChecksumAlgorithm=checksum,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': algorithm,
                        },
                        'BucketKeyEnabled': bucketKeyEnabled
                    },
                ]
            }
        )


def backup_mode(source, source_bucket):
    try:
        source.put_bucket_versioning(
            Bucket=source_bucket
        )
        return True
    except:
        return False


def progress_upload(destination, file_path, destination_bucket, progress_var, remaining_var):
    statinfo = os.stat(file_path)
    total_size = statinfo.st_size

    def upload_progress(chunk):
        progress = int((chunk / total_size) * 100)
        progress_var.set(progress)
        remaining = 100 - progress
        remaining_var.set(remaining)

    destination.upload_file(file_path, destination_bucket, file_path, Callback=upload_progress)


def progress_download(source, source_bucket, file, file_path, progress_var):
    total_bytes = source.head_object(Bucket=source_bucket, Key=file)["ContentLength"]
    bytes_transferred = 0

    def download_progress(chunk):
        nonlocal bytes_transferred
        bytes_transferred += len(chunk)
        progress = int((bytes_transferred / total_bytes) * 100)
        progress_var.set(progress)

    storage_class = source.head_object(Bucket=source_bucket, Key=file)["StorageClass"]

    if storage_class in ["STANDARD", "INTELLIGENT_TIERING", "ONEZONE_IA"]:
        source.download_file(source_bucket, file, file_path, Callback=download_progress)
    else:
        with open(file_path, "wb") as f:
            response = source.get_object(Bucket=source_bucket, Key=file)
            body = response["Body"]
            chunk_size = 1024 * 1024  # 1 MB chunk size
            while True:
                chunk = body.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                download_progress(chunk)


def get_download_client(source):
    session = boto3.Session(profile_name=source)
    return session.client('s3')


def get_upload_client(destination):
    session = boto3.Session(profile_name=destination)
    return session.client('s3')


def transfer_files(source_profile, destination_profile, source_bucket, destination_bucket, delete_files, progress_var, remaining_var):
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting transfer_files")

    try:
        cache = "/tmp/"
        source_session = boto3.Session(profile_name=source_profile)
        destination_session = boto3.Session(profile_name=destination_profile)

        source_client = source_session.client('s3')
        destination_client = destination_session.client('s3')

        logger.info("Getting source bucket contents")
        paginator = source_client.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(Bucket=source_bucket)

        total_files = []
        for response in response_iterator:
            if 'Contents' in response:
                total_files.extend([obj['Key'] for obj in response['Contents']])

        total_progress = len(total_files)
        current_progress = 0

        logger.info("Starting file transfer")
        for file in total_files:
            current_progress += 1
            progress_var.set(current_progress)
            remaining = 100 - ((current_progress / total_progress) * 100)
            remaining_var.set(remaining)

            logger.info(f"Transferring file: {file}")
            file_path = os.path.join(cache, file)

            progress_download(source_client, source_bucket, file, file_path, progress_var)

            destination_client.upload_file(file_path, destination_bucket, file)

            if delete_files:
                logger.info(f"Deleting file from source bucket: {file}")
                source_client.delete_object(Bucket=source_bucket, Key=file)

            os.remove(file_path)

        logger.info("File transfer complete")

    except Exception as e:
        logger.error("An error occurred during file transfer:")
        logger.error(str(e))
        logger.error(traceback.format_exc())

    logger.info("Finished transfer_files")
