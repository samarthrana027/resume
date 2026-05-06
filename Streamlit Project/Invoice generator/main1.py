import pandas as pd


customers_info=pd.read_csv("customers.csv")

print(f"custoemers address = {customers_info['Address'].tolist()} ")