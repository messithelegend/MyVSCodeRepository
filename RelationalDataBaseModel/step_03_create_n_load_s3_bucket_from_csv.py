### This program would take Accounts.csv, Customers.csv, Transactions.csv and Loans.csv from local
### and upload them to an S3 bucket named 'pat-relational-database-bucket-1'.

import pandas as pd
import numpy as np
import boto3  ### For interacting with AWS services
from botocore.exceptions import NoCredentialsError, ClientError
from step_01_ReadAccessKey import get_aws_keys  # Import the function to get AWS keys

access_key, secret_key = get_aws_keys('PatAITesting_accessKeys.csv')

# Print the keys (for debugging purposes)
# print("AWS Access Key:", access_key)
# print("AWS Secret Key:", secret_key)

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# Function to create an S3 bucket if it doesn't exist
def create_bucket_if_not_exists(bucket_name):
    """
    Creates an S3 bucket if it does not already exist.
    :param bucket_name: The name of the bucket to create.
    """
    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        # If the bucket does not exist, create it
        if e.response['Error']['Code'] == '404':
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Error checking bucket: {e}")
            raise

def upload_to_s3(file_name, bucket_name, s3_file_name):
    """
    Uploads a file to an S3 bucket.
    :param file_name: The local file to upload.
    :param bucket_name: The name of the S3 bucket.
    :param s3_file_name: The name of the file in the S3 bucket.
    """
    try:
        s3_client.upload_file(file_name, bucket_name, s3_file_name)
        print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' as '{s3_file_name}'.")
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
    except NoCredentialsError:
        print("Credentials not available.")

# Main execution
if __name__ == "__main__":
    BUCKET_NAME = "pat-relational-database-bucket-1"  # Replace with your desired bucket name
    # Step 1: Create the S3 bucket if it doesn't exist
    create_bucket_if_not_exists(BUCKET_NAME)

    # Step 2: Upload the CSV file to the S3 bucket
    CSV_FILE_NAME = 'RelationalDataBaseModel/Accounts.csv'  # Replace with your CSV file path
    upload_to_s3(CSV_FILE_NAME, BUCKET_NAME, "accounts/Accounts.csv")

    CSV_FILE_NAME = 'RelationalDataBaseModel/Customers.csv'  # Replace with your CSV file path
    upload_to_s3(CSV_FILE_NAME, BUCKET_NAME, "customers/Customers.csv") 

    CSV_FILE_NAME = 'RelationalDataBaseModel/Loans.csv'  # Replace with your CSV file path
    upload_to_s3(CSV_FILE_NAME, BUCKET_NAME, "loans/Loans.csv")
    
    CSV_FILE_NAME = 'RelationalDataBaseModel/Transactions.csv'  # Replace with your CSV file path
    upload_to_s3(CSV_FILE_NAME, BUCKET_NAME, "transactions/Transactions.csv")

