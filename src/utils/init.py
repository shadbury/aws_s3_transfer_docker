import boto3

def get_buckets(profile):
    session = boto3.Session(profile_name=profile)
    s3 = session.resource('s3')
    bucket_names = [bucket.name for bucket in s3.buckets.all()]
    return bucket_names

def transfer_files(source_profile, destination_profile, source_bucket, destination_bucket,
                   encrypt_source=False, encrypt_destination=False, encryption_algorithm=None):
    source_session = boto3.Session(profile_name=source_profile)
    destination_session = boto3.Session(profile_name=destination_profile)

    source_s3 = source_session.resource('s3')
    destination_s3 = destination_session.resource('s3')

    source_bucket_obj = source_s3.Bucket(source_bucket)
    destination_bucket_obj = destination_s3.Bucket(destination_bucket)

    for obj in source_bucket_obj.objects.all():
        source_key = obj.key
        destination_key = source_key

        if encrypt_source:
            source_key = f"{encryption_algorithm}/{source_key}"

        if encrypt_destination:
            destination_key = f"{encryption_algorithm}/{destination_key}"

        source_bucket_obj.copy({'Bucket': source_bucket, 'Key': source_key},
                               destination_bucket_obj.name, destination_key)
