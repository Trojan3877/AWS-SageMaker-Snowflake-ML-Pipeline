# src/data_loader.py

import snowflake.connector
import pandas as pd
import os

def load_data_from_snowflake():
    """
    Connects to Snowflake securely using environment variables and loads transaction data.
    """
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )
    
    query = "SELECT * FROM transactions LIMIT 10000;"  # Example table
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df

