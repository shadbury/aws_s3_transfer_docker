import boto3
import aws


def copy_object(source_profile, source_bucket, source_key, destination_profile, destination_bucket):
    """
    Copy an object from the source bucket to the destination bucket.
    """
    session = boto3.Session(profile_name=source_profile)
    s3_source = session.resource("s3")
    s3_destination = session.resource("s3")

    s3_destination.Object(destination_bucket, source_key).copy_from(
        CopySource={"Bucket": source_bucket, "Key": source_key}
    )


def delete_object(profile, bucket, key):
    """
    Delete an object from the specified bucket.
    """
    session = boto3.Session(profile_name=profile)
    s3 = session.resource("s3")
    s3.Object(bucket, key).delete()


def encrypt_object(profile, bucket, key, algorithm):
    """
    Encrypt an object in the specified bucket with the appropriate algorithm.
    """
    session = boto3.Session(profile_name=profile)
    s3 = session.resource("s3")

    # Check if the bucket is already encrypted
    if not aws.is_bucket_encrypted(profile, bucket):
        # Check the encryption algorithm specified
        if algorithm == "AES256":
            # Encrypt the object with AES256 algorithm
            s3.Object(bucket, key).copy_from(
                CopySource={"Bucket": bucket, "Key": key},
                ServerSideEncryption="AES256"
            )
            print(f"Object '{key}' in bucket '{bucket}' encrypted with AES256 algorithm.")
        elif algorithm == "KMS":
            # Encrypt the object with KMS algorithm
            s3.Object(bucket, key).copy_from(
                CopySource={"Bucket": bucket, "Key": key},
                ServerSideEncryption="aws:kms"
            )
            print(f"Object '{key}' in bucket '{bucket}' encrypted with KMS algorithm.")
        else:
            print(f"Invalid encryption algorithm: {algorithm}")
    else:
        print(f"Bucket '{bucket}' is already encrypted.")
