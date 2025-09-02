import pandas as pd
import numpy as np
import openpyxl
from faker import Faker

### Create a sample dataset using faker
fake = Faker()
data = {
    "FirstName": [fake.first_name() for _ in range(1000)],
    "LastName": [fake.last_name() for _ in range(1000)],
    "Age": np.random.randint(18, 70, size=1000),
    "City": [fake.city() for _ in range(1000)],
    "Salary": np.random.randint(30000, 120000, size=1000),
    "Status": np.random.choice(['Single', 'Married', 'Divorced'], size=1000),
    "BankBalance": np.round(np.random.uniform(10000, 10000000, size=1000),2),
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
df.to_excel("StockData.xlsx", index=False)
df.to_csv("StockData.csv", index=False)