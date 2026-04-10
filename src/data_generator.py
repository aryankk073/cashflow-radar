import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_bank_data(days=730):
    # Start 2 years ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    balance = 5000.0
    data = []
    
    # Set a random seed so your team gets the exact same data
    np.random.seed(42)
    
    for date in dates:
        # 1. Salary Deposit (Monthly on the 1st)
        if date.day == 1:
            amount = 3000.0
            type = 'Salary'
            balance += amount
        # 2. Rent Payment (Monthly on the 2nd)
        elif date.day == 2:
            amount = -1200.0
            type = 'Rent'
            balance += amount
        # 3. Weekly Groceries (Every Monday)
        elif date.weekday() == 0:
            amount = -np.random.uniform(80, 150)
            type = 'Groceries'
            balance += amount
        # 4. Weekend Fun (Fri/Sat)
        elif date.weekday() in [4, 5]:
            amount = -np.random.uniform(20, 200)
            type = 'Entertainment'
            balance += amount
        # 5. Random daily expenses
        else:
            amount = -np.random.uniform(5, 40)
            type = 'Miscellaneous'
            balance += amount
            
        data.append([date, balance, type])
    
    # Create the dataframe using 'ds' (date) and 'y' (value) which Prophet requires
    df = pd.DataFrame(data, columns=['ds', 'y', 'type'])
    
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    df.to_csv('data/historical_balances.csv', index=False)
    print("SUCCESS: data/historical_balances.csv created with 2 years of data.")

if __name__ == "__main__":
    generate_bank_data()