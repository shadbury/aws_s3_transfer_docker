import os
import configparser
import boto3


class AWS:
    @staticmethod
    def get_config_profiles():
        config_file = os.path.expanduser("~/.aws/config")
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            profiles = config.sections()
            return profiles
        return []

    @staticmethod
    def get_credentials_profiles():
        credentials_file = os.path.expanduser("~/.aws/credentials")
        if os.path.exists(credentials_file):
            config = configparser.ConfigParser()
            config.read(credentials_file)
            profiles = config.sections()
            return profiles
        return []

    @staticmethod
    def get_bucket_list(profile):
        session = boto3.Session(profile_name=profile)
        s3_client = session.client("s3")
        response = s3_client.list_buckets()
        bucket_list = [bucket["Name"] for bucket in response.get("Buckets", [])]
        return bucket_list

    @staticmethod
    def is_bucket_encrypted(profile, bucket):
        session = boto3.Session(profile_name=profile)
        s3_client = session.client("s3")
        response = s3_client.get_bucket_encryption(Bucket=bucket)
        encryption_rules = response.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
        return len(encryption_rules) > 0

    @staticmethod
    def encrypt_bucket(profile, bucket):
        session = boto3.Session(profile_name=profile)
        s3_client = session.client("s3")
        encryption_configuration = {
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }
        s3_client.put_bucket_encryption(Bucket=bucket, ServerSideEncryptionConfiguration=encryption_configuration)
