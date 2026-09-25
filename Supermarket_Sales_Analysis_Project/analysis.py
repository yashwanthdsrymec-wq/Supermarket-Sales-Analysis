import pandas as pd
from pathlib import Path

DATA = Path(__file__).parent / "data" / "supermarket_sales.csv"
df = pd.read_csv(DATA)

df["Calculated Sales"] = df["Quantity"] * df["Unit Price"]
df["Difference"] = (df["Sales"] - df["Calculated Sales"]).round(2)

print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nTop product:")
print(df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5))
print("\nBranch sales:")
print(df.groupby(["Branch", "City"])["Sales"].sum().sort_values(ascending=False))
print("\nCategory sales:")
print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False))
print("\nPayment transactions:")
print(df["Payment"].value_counts())
print("\nAverage sale by customer type:")
print(df.groupby("Customer Type")["Sales"].mean())
print("\nAverage rating:", round(df["Rating"].mean(), 2))
print("\nSales calculation mismatches:", (df["Difference"].abs() > 0.01).sum())
