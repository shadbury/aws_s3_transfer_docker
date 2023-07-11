import boto3
import configparser
import os
import logging


def get_profiles(source="config"):
    if source == "config":
        config_file_path = os.path.expanduser("~/.aws/config")
    else:
        config_file_path = os.path.expanduser("~/.aws/credentials")

    profiles = set()

    if os.path.exists(config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path)

        if "default" in config.sections():
            config.remove_section("default")

        for section in config.sections():
            if section.lower() != "default":
                profile_name = section.split("profile ")[-1]
                profiles.add(profile_name)

    return list(profiles)





def get_buckets(profile):
    # Retrieve buckets using the given profile
    try:
        session = boto3.Session(profile_name=profile)
        s3_client = session.client("s3")
        response = s3_client.list_buckets()
        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        return buckets
    except Exception as e:
        logging.error(f"Error retrieving buckets: {str(e)}")
        return []


def transfer_files(source_profile, destination_profile, source_bucket, destination_bucket,
                   encrypt_source=False, encrypt_destination=False, encryption_algorithm=None):
    # Perform file transfer based on the specified parameters
    try:
        source_session = boto3.Session(profile_name=source_profile)
        source_s3_client = source_session.client("s3")
        destination_session = boto3.Session(profile_name=destination_profile)
        destination_s3_client = destination_session.client("s3")

        copy_source = {"Bucket": source_bucket, "Key": ""}
        destination_key_prefix = ""

        if encrypt_source:
            copy_source["ServerSideEncryption"] = encryption_algorithm

        if encrypt_destination:
            destination_key_prefix = encryption_algorithm + "/"

        response = source_s3_client.list_objects_v2(Bucket=source_bucket)

        for obj in response.get("Contents", []):
            source_key = obj["Key"]
            destination_key = destination_key_prefix + source_key
            source = {"Bucket": source_bucket, "Key": source_key}
            destination = {"Bucket": destination_bucket, "Key": destination_key}

            source_s3_client.copy_object(
                CopySource=source, Bucket=destination_bucket, Key=destination_key
            )

            if encrypt_destination:
                destination_s3_client.put_object(
                    Bucket=destination_bucket,
                    Key=destination_key,
                    ServerSideEncryption=encryption_algorithm,
                )

            source_s3_client.delete_object(Bucket=source_bucket, Key=source_key)
    except Exception as e:
        logging.error(f"Error transferring files: {str(e)}")
