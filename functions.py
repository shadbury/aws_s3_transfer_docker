import boto3
import os
import progressbar
from botocore.exceptions import NoCredentialsError


# Delete file function

def delete_file(client, bucket, key):
    client.delete_object(
        Bucket=bucket,
        Key=key
)


# Progress bar or file upload
def progress_upload(destination,file_path,destination_bucket):

    # get metadata infomation about current file
    statinfo = os.stat(file_path)

    # initialize progress bad
    up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
    up_progress.start()

    # Update progress bad
    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)

    # updoad file
    destination.upload_file(file_path, destination_bucket, file_path, Callback=upload_progress)

    # upload finished
    up_progress.finish()




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
def get_download_client(source):
    source = boto3.Session(profile_name=source)
    return source.client('s3')


# Get the boto3 s3 client for the bucket to receive the content
def get_upload_client(destination):
    source = boto3.Session(profile_name=destination)
    return source.client('s3')


# Create the transfer process
def transfer(source, destination, source_bucket, destination_bucket, delete_source_files):

    # Temp location to store files for transfer
    cache = "/tmp/"

    # Setup the source client
    source = get_download_client(source)

    # Setup the destination client
    destination = get_upload_client(destination)

    # Grap bucket with list of objects
    bucket = source.list_objects(
        Bucket=source_bucket
    )

    # Get the name values of the files in the cache directory
    for value in bucket['Contents']:
        file = value['Key']

        # If the current file name doesn't exist, proceed.
        if file not in cache:

            # get the file path
            file_path = "{}{}".format(cache,file)


            # display to use the the application is about to attempt to download an object from the source s3 bucket
            print("Downloading: {}".format(file))

            # start the download process
            progress_download(source,source_bucket,file,file_path)

            # display to use the the application is about to attempt to upload an object to the destination s3 bucket
            print("Uploading: {}".format(file))

            # start the upload process
            progress_upload(destination, file_path, destination_bucket)

            # if the delete source files option was true. delete the file from the source s3 bucket
            if delete_source_files:
                print("deleting file from source bucket: {}".format(file))
                delete_file(source, bucket['Name'], file)

            # remove files from cache after upload is complete
            print("deleting file from cache: {}".format(file))
            os.remove(cache+file)
