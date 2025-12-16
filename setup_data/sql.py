import pandas as pd
import sqlite3
import os

df = pd.read_csv("../data/sales_data.csv")
conn = sqlite3.connect("../sales.db")

df.to_sql(
    name="sales_transactions",
    con=conn,
    if_exists="replace",
    index=False
)

conn.close()
