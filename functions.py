import boto3
import os
import progressbar
from botocore.exceptions import NoCredentialsError

def progress_download(source,source_bucket,file,file_path):
    
    # Get the object
    response = source.head_object(Bucket=source_bucket, Key=file)
    
    # Get the size of the file
    size = response['ContentLength']

    #initialize the progress bar
    up_progress = progressbar.progressbar.ProgressBar(maxval=size)
    up_progress.start()

    # Update progress
    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)

    try:
        # Start the download
        source.download_file(source_bucket, file, file_path, 
                             Callback=upload_progress)
        
        # When download is finished, update progress
        up_progress.finish()
        print("Download Successful")
        return True
    
    # If the file is not found, print an error
    except FileNotFoundError:
        
        print("The file was not found")
        return False
    
    # If credentials arent setup, print an error
    except NoCredentialsError:

        print("Credentials not available")
        return False



# Get the boto3 s3 client for the content to be downloaded
def get_download_client():
    source = boto3.Session(profile_name='wellteqnib-prod')
    return source.client('s3')


# Get the boto3 s3 client for the bucket to receive the content
def get_upload_client():
    source = boto3.Session(profile_name='default')
    return source.client('s3')


# Create the transfer process
def transfer(source, destination, source_bucket, destination_bucket):

    # Temp location to store files for transfer
    cache = "/tmp/"

    # Setup the source client
    source = get_download_client()

    # Setup the destination client
    destination = get_upload_client()

    # Grap bucket with list of objects
    bucket = source.list_objects(
        Bucket=source_bucket
    )

    # Get the name values of the files in the cache directory
    for value in bucket['Contents']:
        file = value['Key']

        # If the current file name doesn't exist, proceed.
        if file not in cache:
            print("Downloading: {}".format(file))
            file_path = "{}{}".format(cache,file)
            print("Uploading: {}".format(file))
            progress_download(source,source_bucket,file,file_path)
            destination.upload_file((cache+file), destination_bucket, file)
            os.remove(cache+file)
