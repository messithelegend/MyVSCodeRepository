import pandas as pd
import numpy as np
from faker import Faker
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from ReadAccessKey import get_aws_keys  # Import the function to get AWS keys

# Get the AWS keys from the CSV file
access_key, secret_key = get_aws_keys('PatAITesting_accessKeys.csv')

# Print the keys (for debugging purposes)
print("AWS Access Key:", access_key)
print("AWS Secret Key:", secret_key)

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

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

def generate_csv(file_name):
    """
    Generates a sample CSV file using Faker and pandas.
    :param file_name: The name of the CSV file to generate.
    """
    fake = Faker()
    data = {
        "FirstName": [fake.first_name() for _ in range(1000)],
        "LastName": [fake.last_name() for _ in range(1000)],
        "Age": np.random.randint(18, 70, size=1000),
        "City": [fake.city() for _ in range(1000)],
        "Salary": np.random.randint(30000, 120000, size=1000),
        "Status": np.random.choice(['Single', 'Married', 'Divorced'], size=1000),
        "BankBalance": np.round(np.random.uniform(10000, 10000000, size=1000), 2),
        "BankName": [fake.company() + " Bank" for _ in range(1000)],
        "StockSymbol": [fake.lexify(text='???') for _ in range(1000)],
        "StockPrice": np.round(np.random.uniform(10, 1000, size=1000), 2),
        "StockPriceOneYearAgo": np.round(np.random.uniform(10, 1000, size=1000), 2),
        "StockVolume": np.random.randint(100, 100000, size=1000),
        "StockPriceYearAgo": np.round(np.random.uniform(10, 1000, size=1000), 2),
        "StockPriceSixMonthsAgo": np.round(np.random.uniform(10, 1000, size=1000), 2),
        "StockPriceThreeMonthsAgo": np.round(np.random.uniform(10, 1000, size=1000), 2),
        "StockPriceOneMonthAgo": np.round(np.random.uniform(10, 1000, size=1000), 2)
    }

    df = pd.DataFrame(data)
    print(df.shape)
    print(df.head())
    df.to_csv(file_name, index=False)
    print(f"CSV file '{file_name}' generated.")

# Main execution
if __name__ == "__main__":
    BUCKET_NAME = "pathikrith-stock-data-bucket-1"  # Replace with your desired bucket name
    CSV_FILE_NAME = "StockData.csv"  # Name of the CSV file to generate and upload

    # Step 1: Create the S3 bucket if it doesn't exist
    create_bucket_if_not_exists(BUCKET_NAME)

    # Step 2: Generate the CSV file
    generate_csv(CSV_FILE_NAME)

    # Step 3: Upload the CSV file to the S3 bucket
    upload_to_s3(CSV_FILE_NAME, BUCKET_NAME, CSV_FILE_NAME)