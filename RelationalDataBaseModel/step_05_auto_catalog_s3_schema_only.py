## This program would auto catalog all the files in the S3 bucket named 
# 'pat-relational-database-bucket-1'.
import boto3  ### For interacting with AWS services
import awswrangler as wr  ### For interacting with AWS services, especially Athena
import pandas as pd
import json
import os
from openai import OpenAI
from botocore.exceptions import NoCredentialsError, ClientError
from step_01_ReadAccessKey import get_aws_keys  # Import the function to get AWS keys

access_key, secret_key = get_aws_keys('PatAITesting_accessKeys.csv')

## Configure the databases as in aethna
DATABASE = "relational_database_1_csv_for_metadata"
TABLES = ["accounts", "customers", "loans", "transactions"]
OUTPUT_FILE = "base_auto_catalog.json"
ATHENA_OUTPUT = "s3://pat-relational-database-bucket-1/athena-results/"
REGION = "us-east-1"

# Initialize the athena helper client
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name= REGION
)

# List all the tables in the database

tables = wr.catalog.get_tables(database=DATABASE, boto3_session=session)

# Collect the schema information for each table (column + type + comments)
catalog = []
for table in tables:
    table_name = table["Name"]
    print(f'Processing table: {table_name}')
    desc = wr.catalog.get_table_description(
        database=DATABASE,
        table=table_name,
        boto3_session=session)
    print('\n')
    print(f"Description of table: {desc}")
#Extract columns
    cols = desc['StorageDescriptor']['Columns']
    for col in cols:
        catalog.append({
            'table': table_name,
            'column': col.get['Name'],
            'type': col.get['Type'],
            'comment': col.get('Comment', '')
        })

# Save the catalog to a JSON file
df_catalog = pd.DataFrame(catalog)
print(f'Catalog DataFrame: {df_catalog}')
