import pandas as pd
import random
from faker import Faker

# initialize Faker and random with a seed for reproducibility
SEED = 42
faker = Faker()
Faker.seed(SEED)
random.seed(SEED)

#Parameters
n_customers = 5000
n_accounts = 10000
n_transactions = 50000
n_loans = 2000

# Generate Customers Data
employment_statuses = ['Employed', 'Unemployed', 'Self-Employed', 'Student', 'Retired'] 
customers = []
for i in range(1, n_customers + 1):
    customers.append({
        'CustomerID': i,
        'FirstName': faker.first_name(),
        'LastName': faker.last_name(),
        'Email': faker.email(),
        'PhoneNumber': faker.phone_number(),
        'Address': faker.address().replace('\n', ', '),
        'DateOfBirth': faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
        'EmploymentStatus': random.choice(employment_statuses),
        'AnnualIncome': round(random.uniform(20000, 150000), 2) 
    })
customers_df = pd.DataFrame(customers)
customers_df.to_csv('Customers.csv', index=False)

# Generate Accounts Data
account_types = ['Savings', 'Checking', 'Credit Card', 'Loan']
status = ['Active', 'Closed', 'Suspended', 'Pending', 'Dormant']
accounts = []
for i in range(1, n_accounts + 1):
    accounts.append({
        'AccountID': i,
        'CustomerID': random.randint(1, n_customers),
        'AccountNumber': faker.unique.bban(),
        'AccountType': random.choice(account_types),
        'Branch': faker.city(),
        'BranchCode': faker.swift8(),
        'Balance': round(random.uniform(0, 100000), 2),
        'OpenDate': faker.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d'),
        'Status': random.choice(status)
    })
accounts_df = pd.DataFrame(accounts)
accounts_df.to_csv('Accounts.csv', index=False)

# Generate Transactions Data
transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Fee', 'Interest', 'Refund']
channels = ['Online', 'Branch', 'ATM', 'Mobile', 'Phone']
currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'INR']

transactions = []
for i in range(1, n_transactions + 1):
    transactions.append({
        'TransactionID': i,
        'AccountID': random.randint(1, n_accounts),
        'TransactionType': random.choice(transaction_types),
        'Amount': round(random.uniform(1, 10000), 2),
        'Merchant': faker.company(),
        'MerchantCategory': faker.bs().split()[0].title(),
        'Description': faker.sentence(nb_words=6),
        'Currency': random.choice(currencies),
        'TransactionDate': faker.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
        'Channel': random.choice(channels)
    })  
transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv('Transactions.csv', index=False)

# Generate Loans Data
loan_types = ['Personal', 'Home', 'Car', 'Business', 'Education', 'Payday', 'Mortgage']
loan_statuses = ['Approved', 'Pending', 'Rejected', 'Closed', 'Defaulted']
loans = []
for i in range(1, n_loans + 1):
    loans.append({
        'LoanID': i,
        'CustomerID': random.randint(1, n_customers),
        'LoanType': random.choice(loan_types),
        'PrincipalAmount': round(random.uniform(1000, 50000), 2),
        'InterestRate': round(random.uniform(3.0, 15.0), 2),
        'StartDate': faker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
        'EndDate': faker.date_between(start_date='today', end_date='+5y').strftime('%Y-%m-%d'),
        'MonthlyInstallment': round(random.uniform(100, 2000), 2),
        'TotalPayable': round(random.uniform(1200, 60000), 2),
        'Collateral': faker.word().title(),
        'Status': random.choice(loan_statuses)
    })
loans_df = pd.DataFrame(loans)
loans_df.to_csv('Loans.csv', index=False)
print("CSV files generated: Customers.csv, Accounts.csv, Transactions.csv, Loans.csv")