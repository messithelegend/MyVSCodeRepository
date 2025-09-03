import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def check_s3_access():
    try:
        # Initialize the S3 client
        s3_client = boto3.client('s3')
        
        # List all S3 buckets
        response = s3_client.list_buckets()
        print("S3 Access Verified. Buckets in your account:")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")
    except NoCredentialsError:
        print("No AWS credentials found. Please configure your credentials.")
    except ClientError as e:
        print(f"Error accessing S3: {e}")

# Run the check
check_s3_access()