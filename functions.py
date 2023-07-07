import os
import time
import logging
import boto3
from botocore.exceptions import NoCredentialsError
import traceback
import progressbar
from tkinter import messagebox
import tempfile
import shutil



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


def progress_upload(destination, file_path, destination_bucket, file_name, progress_var):
    statinfo = os.stat(file_path)
    total_size = statinfo.st_size

    def upload_progress(chunk):
        progress = int((chunk / total_size) * 100)
        progress_var.set(progress)

    destination.upload_file(file_path, destination_bucket, file_name, Callback=upload_progress)




def progress_download(source_client, source_bucket, file, file_path, progress_var):
    try:
        response = source_client.head_object(Bucket=source_bucket, Key=file)
        storage_class = response.get('StorageClass')

        if storage_class == 'GLACIER':
            # If the object is in Glacier storage class, initiate a restore request
            response = source_client.restore_object(
                Bucket=source_bucket,
                Key=file,
                RestoreRequest={'Days': 7}
            )
            print(f"Initiated restore request for object {file}")
            return

        # Extract the file name from the object key
        file_name = os.path.basename(file)

        # Check if the file already exists and delete it if it does
        if os.path.exists(file_path):
            os.remove(file_path)

        # Create the directory structure if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Download the object
        try:
            source_client.download_file(
                Bucket=source_bucket,
                Key=file,
                Filename=file_path,
                Callback=lambda bytes_transferred: progress_var.set(bytes_transferred)
            )
            print(f"Downloaded file: {file_path}")
        except Exception as e:
            print(f"Error occurred during file download: {e}")
    except Exception as e:
        print(f"Error occurred while getting object information: {e}")



def get_download_client(source):
    session = boto3.Session(profile_name=source)
    return session.client('s3')


def get_upload_client(destination):
    session = boto3.Session(profile_name=destination)
    return session.client('s3')


# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")




def transfer_files(source_profile, destination_profile, source_bucket, destination_bucket, delete_files, progress_var, remaining_var):
    # Create Boto3 clients for the source and destination profiles
    source_session = boto3.Session(profile_name=source_profile)
    destination_session = boto3.Session(profile_name=destination_profile)
    source_client = source_session.client('s3')
    destination_client = destination_session.client('s3')

    # Get the list of objects in the source bucket
    response = source_client.list_objects_v2(Bucket=source_bucket)
    objects = response['Contents']

    # Calculate the total number of objects for progress tracking
    total_objects = len(objects)
    processed_objects = 0

    # Create a temporary directory for file downloads
    temp_directory = os.path.join('/tmp/proj_temp', source_bucket)

    try:
        for obj in objects:
            # Get the object key
            file_key = obj['Key']

            # Create the destination file path
            file_path = os.path.join(temp_directory, file_key)

            # Download the object from the source bucket
            try:
                progress_download(source_client, source_bucket, file_key, file_path, progress_var)
                print(f"Downloaded object: {file_key}")
            except Exception as e:
                print(f"Error occurred during file download: {e}")
                continue

            # Upload the downloaded object to the destination bucket
            try:
                file_name = os.path.basename(file_key)
                destination_key = os.path.join(os.path.dirname(file_key), file_name)  # Include directory structure
                progress_upload(destination_client, file_path, destination_bucket, destination_key, progress_var)
                print(f"Uploaded object: {file_key}")
            except Exception as e:
                print(f"Error occurred during file upload: {e}")
                continue

            processed_objects += 1
            remaining_objects = total_objects - processed_objects
            remaining_var.set(remaining_objects)

            # Delete the downloaded file if specified
            if delete_files:
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_key}")
                except Exception as e:
                    print(f"Error occurred while deleting file: {e}")

    finally:
        # Remove the temporary directory
        shutil.rmtree(temp_directory)

