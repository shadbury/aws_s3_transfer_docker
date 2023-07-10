import boto3

def check_profile_access(profile):
    try:
        # Create a session with the selected profile
        session = boto3.Session(profile_name=profile)
        
        # Perform a simple operation to check if the user has access
        s3_client = session.client("s3")
        s3_client.list_buckets()
        
        # If the operation succeeds, return True to indicate access
        return True
    except Exception:
        # If the operation fails, return False to indicate no access
        return False
