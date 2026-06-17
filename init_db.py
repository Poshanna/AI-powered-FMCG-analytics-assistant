
import sqlite3
import pandas as pd
import os

def create_database():
    db_path = "fmcg.db"
    
    conn = sqlite3.connect(db_path)
    
    csv_files = {
        "sales": "sales.csv",
        "inventory": "inventory.csv",
        "products": "products.csv",
        "stores": "stores.csv"
    }
    
    for table_name, csv_file in csv_files.items():
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Loaded {len(df)} rows into {table_name}")
        else:
            print(f"CSV file {csv_file} not found!")
    
    conn.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()
