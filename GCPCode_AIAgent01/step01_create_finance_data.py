import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from random import randint

#Initialize Faker library for generating realistic data
fake = Faker()

#Configuartion variables # as if it is a small community bank
NUM_CUSTOMERS = 50000
NUM_BRANCHES = 100
NUM_PRODUCTS = 100
NUM_ACCOUNTS = 100000
NUM_TRANSACTIONS = 1000000

#Generate a list of fake branch ids
def generate_branch_data():
    data = []
    # Create NUM_BRANCHES distinct branches
    for branch_id in range(1, NUM_BRANCHES + 1):
        data.append({
            'branch_id': branch_id,
            'branch_name': f"Branch {random.choice(['North', 'South', 'Central', 'East', 'West'])} {branch_id}",
            'manager_name': fake.name(),
            'branch_address': fake.street_address(),
            'branch_city': fake.city(),
            'branch_state': fake.state_abbr(),
            'phone_number': fake.phone_number(),
            'operating_hours': '9:00 AM - 5:00 PM',
            'established_date': fake.date_between(start_date='-20y', end_date='-4y'),
            'total_employees': randint(10, 100),
            'ATM_count': randint(5, 15),
            'average_rating': round(random.uniform(3.5, 5.0), 1)
        })
    return pd.DataFrame(data)

#Function to generate fake product data
def generate_product_data():
    product_types = ['Savings', 'Checking', 'Credit Card', 'Loan', 'CD']
    data = []
    # Create NUM_PRODUCTS distinct products
    for product_id in range(1, NUM_PRODUCTS + 1):
        product_type = random.choice(product_types)
        data.append({
            'product_id': product_id,
            'product_name': f"{random.choice(['Basic', 'Premium', 'Elite', 'Student'])} {product_type}",
            'product_type': product_type,
            'description': fake.catch_phrase(),
            'launch_date': fake.date_between(start_date='-20y', end_date='-1y'),
            'maturity_period': random.choice([0, 6, 12, 24]) if product_type == 'CD' else 0,
            'minimum_deposite': round(random.uniform(0, 1000), 2) if product_type != 'Loan' else 0,
            'annual_fee': round(random.uniform(0, 150), 2),
            'interest_rate': round(random.uniform(1.0, 8.0), 2),
            'transaction_fee': round(random.uniform(1, 5), 2),
            'minimum_balance': random.choice([0, 100, 500, 1000]),
            'maximum_withdrawal': random.choice([10000, 50000, 100000, 500000]),
            'maximum_deposit': random.choice([10000, 50000, 100000, 500000]),
            'risk_level': random.randint(1, 5),
            'is_new_product': random.choice([True, False]),
            'discontinued_date': None

        })
    return pd.DataFrame(data)

# Function to generate fake customer data
def generate_customer_data():
    data = []
    # Create NUM_CUSTOMERS distinct customers
    for customer_id in range(1, NUM_CUSTOMERS + 1):
        date_joined = fake.date_between(start_date='-20y',)
        data.append({
            'customer_id': customer_id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.unique.email(),
            'phone_number': fake.phone_number(),
            'street_address': fake.street_address(),
            'city': fake.city(),
            'state_province': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
            'occupation': fake.job(),
            'annual_income': round(random.uniform(20000, 200000), 2),
            'credit_score': random.randint(300, 850),
            'marital_status': random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
            'is_active': random.choice([True, False]),
            'date_joined': date_joined,
            'last_login': fake.date_time_between(start_date=date_joined, end_date='now'),
            'last_updated': fake.date_time_between(start_date='-1y', end_date='now'),
        })
    return pd.DataFrame(data)

# Function to generate fake account data (requires customer_ids, branch_ids, and product_ids)
def generate_account_data(customer_df, branch_df, product_df):
    customer_ids = customer_df['customer_id'].tolist()
    branch_ids = branch_df['branch_id'].tolist()
    product_ids = product_df['product_id'].tolist()
    data = []
    # Create NUM_ACCOUNTS distinct accounts
    for account_id in range(1, NUM_ACCOUNTS + 1):
        #Enforce FK relationships: randomly select existing ids
        customer_id = random.choice(customer_ids)
        branch_id = random.choice(branch_ids)
        product_id = random.choice(product_ids)

        # Get the customer's join date to ensure the account open date is after
        customer_join_date = customer_df[customer_df['customer_id'] == customer_id]['date_joined'].iloc[0]
        open_date = fake.date_between_dates(date_start=customer_join_date)
        current_balance = round(random.uniform(100, 100000), 2)

    data.append({
            'account_id': account_id,
            'customer_id': customer_id,
            'branch_id': branch_id,
            'product_id': product_id,
            'open_date': open_date,
            'current_balance': current_balance,
            'account_type': random.choice(['Savings', 'Checking', 'Credit Card', 'Loan', 'CD']),
            'status': random.choice(['Active', 'Closed', 'Frozen', 'Dormant', 'Under Review']),
            'interest_rate': round(random.uniform(1.0, 8.0), 2),
            'overdraft_limit': round(random.uniform(0, 10000), 2),
            'last_activity_date': fake.date_between_dates(date_start=open_date, date_end='now'),
            'monthly_fee': round(random.uniform(0.0, 10.0), 2),
            'is_joint_account': random.choice([True, False]),
        })        

    return pd.DataFrame(data)

# Function to generate transaction data (requires account_ids)
def generate_transaction_data(account_df):
    account_ids = account_df['account_id'].tolist()
    transaction_types = ['Deposit', 'Withdrawal', 'Purchase', 'Transfer']
    categories = ['Groceries', 'Salary', 'Rent', 'Utilities', 'Travel', 'Dining', 'Investment', 'Entertainment', 'Sports', 'Fees']

    data = []
    # Create NUM_TRANSACTIONS distinct transactions
    for transaction_id in range(1, NUM_TRANSACTIONS + 1):
        #Enforce FK relationship: randomly select existing ids
        account_id = random.choice(account_ids)

        tx_type = random.choice(transaction_types)
        amount = round(random.uniform(1.0, 5000.0), 2)

        # Determine the sign of the amount based on transaction type
        if tx_type == ['Purchase', 'Withdrawl']:
            amount = -abs(amount)
        
        # Ensure transaction time is recent (last 3 years)
        transaction_date_time = fake.date_time_between(start_date='-3y', end_date='now')

        data.append({
            'transaction_id': transaction_id,
            'account_id': account_id,    # FK
            'transaction_type': tx_type,
            'amount': amount,
            'transaction_date_time': transaction_date_time,
            'merchant_name': fake.company() if tx_type != 'Deposit' else 'Payroll Deposit',
            'category': random.choice(categories),
            'status': 'Completed',
            'reference_number': fake.uuid4(),
            'description': fake.text(max_nb_chars=50),
            'location_city': fake.city(),
            'is_international': random.choice([True, False, False, False]), # Mostly domestic
        })

    return pd.DataFrame(data)

# -- Main function

if __name__ == "__main__":
    print(f'Starting synthetic data generation for {NUM_CUSTOMERS} customers, {NUM_BRANCHES} branches,\
          {NUM_PRODUCTS} products, {NUM_ACCOUNTS} accounts, and {NUM_TRANSACTIONS} transactions. This will take a while... ')
    
    #1 Generate Parent tables (PKs only)
    branch_df = generate_branch_data()
    product_df = generate_product_data()
    customer_df = generate_customer_data()

    print('Parent tables generated : Branch, Product, Customer')

    #2 Generate Child tables (PKs and FKs)
    account_df = generate_account_data(customer_df, branch_df, product_df)

    print(f"Generated {len(account_df)} accounts.")

    # Generate transactions df (PKs and FKs)
    transaction_df = generate_transaction_data(account_df) ##Grand Child tables

    print(f"Generated {len(transaction_df)} Transaction records.")

    customer_df.to_csv('customers.csv', index=False)
    branch_df.to_csv('branches.csv', index=False)
    product_df.to_csv('products_services.csv', index=False)
    account_df.to_csv('accounts.csv', index=False)
    transaction_df.to_csv('transactions.csv', index=False)

    print("\nSuccessfully created 5 relational CSV files:")
    print(" - customers.csv")
    print(" - branches.csv")
    print(" - products_services.csv")
    print(" - accounts.csv")
    print(" - transactions.csv")
    print("\nThe Foreign Keys (FKs) in the accounts and transactions tables now correctly reference the Primary Keys (PKs)\
           in their parent tables!")