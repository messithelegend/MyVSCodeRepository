## This program would auto catalog all the files in the S3 bucket named 
# 'pat-relational-database-bucket-1'.
import boto3  ### For interacting with AWS services
import pandas as pd
import json
import os
from openai import OpenAI
from botocore.exceptions import NoCredentialsError, ClientError
from step_01_ReadAccessKey import get_aws_keys  # Import the function to get AWS keys

access_key, secret_key = get_aws_keys('PatAITesting_accessKeys.csv')

s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

## Configure the databases as in aethna
DATABASE = "relational_database_1_csv_for_metadata"
TABLES = ["accounts", "customers", "loans", "transactions"]
OUTPUT_FILE = "auto_catalog.json"
ATHENA_OUTPUT = "s3://pat-relational-database-bucket-1/athena-results/"
REGION = "us-east-1"

## Configure the OpenAI client, load the API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")  

# Athena helpers
athena = boto3.client('athena', region_name=REGION,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

def run_athena_query(query, database=DATABASE, output_location=ATHENA_OUTPUT):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': output_location}
    )

    #print (f'printing response: {response}')
    #print(f'query is {query}')

    query_execution_id = response['QueryExecutionId']
    # Wait for the query to complete
    while True:
        query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        query_state = query_status['QueryExecution']['Status']['State']
        if query_state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
    if query_state == 'SUCCEEDED':
        results = athena.get_query_results(QueryExecutionId=query_execution_id)
        rows = []
        for row in results['ResultSet']['Rows']:  # Skip header row
            ddl_columnname = row['Data'][0]['VarCharValue'].strip()
            rows.append(ddl_columnname)

#        cols = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
#        return pd.DataFrame(row, columns=cols)
    else:
        raise Exception(f"Athena query failed with state: {query_state}")
    
    return pd.DataFrame(columns=rows)  # Skip header row
    
### Get the meaning or the description of the columns in the table
def describe_columns(table_name, column_name, sample_values):
    """Ask GPT 5 to guess the meaning of the column based on sample values"""
    prompt = f"""
    You are an expert data analyst. Given the following information about a database column, 
    provide a concise description of its meaning and purpose.

    Table Name: {table_name}
    Column Name: {column_name}
    Sample Values: {', '.join(sample_values)}

    Please guess:
    1. Probable business meaning of the column.
    2. Possible synonyms or alternative names for the column.
    3. Data type meaning (ID, Date, Amount, category etc.)

    Respond with JSON as keys: 'term', 'synonyms', 'data_type'.
    """
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0,
    )
    description = response.choices[0].message['content'].strip()
    return description

## Main function to auto catalog the tables and columns
def auto_catalog():
    catalog = {}

    for table in TABLES:
        print(f"Processing table: {table}")
        # Get column names
        col_query = f"SHOW COLUMNS IN {table};"
        columns_df = run_athena_query(col_query)
        
        catalog[table] = {}
    
        for col in columns_df.columns:
            print(f"Describing column: {col}")
            # Get sample values
            sample_query = f"SELECT DISTINCT {col} FROM {table} WHERE {col} IS NOT NULL LIMIT 10;"
            sample_df = run_athena_query(sample_query)
            sample_values = sample_df[col].dropna().astype(str).tolist()
            
            if not sample_values:
                sample_values = ["No sample values available"]
            
            # Get description from GPT-5
            try:
                description_json = describe_columns(table, col, sample_values)
                description = json.loads(description_json)
            except Exception as e:
                print(f"    Error getting description for column {col}: {e}")
                description = {"term": "Unknown", "synonyms": [], "data_type": "Unknown"}
            
            catalog[table][col] = {
                "description": description.get("term", "No description"),
                "synonyms": description.get("synonyms", []),
                "data_type": description.get("data_type", "Unknown"),
                "sample_values": sample_values
            }
    
    # Save the catalog to a JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(catalog, f, indent=4)
    print(f"Catalog saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    auto_catalog()
