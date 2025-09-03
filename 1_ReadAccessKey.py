import csv

def get_aws_keys(file_name='PatAITesting_accessKeys.csv'):
    """
    Reads the AWS access keys from the given CSV file and returns them.
    :param file_name: The name of the CSV file containing the keys.
    :return: A tuple (access_key, secret_key).
    """
    with open(file_name, 'r', encoding='utf-8-sig') as file:  # Use 'utf-8-sig' to handle BOM
        csv_reader = csv.DictReader(file)
        
        # Iterate through the rows (assuming only one row contains the keys)
        for row in csv_reader:
            access_key = row['Access key ID']  # Match the exact header name
            secret_key = row['Secret access key']  # Match the exact header name
            return access_key, secret_key  # Return the keys as a tuple

    # If no keys are found, raise an exception
    raise ValueError("No access keys found in the file.")