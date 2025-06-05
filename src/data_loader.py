# src/data_loader.py

"""
Data Loader Module
------------------
This module connects to Snowflake and loads transaction data into a pandas DataFrame.
"""

import snowflake.connector
import pandas as pd

def load_data_from_snowflake(user, password, account, warehouse, database, schema, table):
    """
    Connects to Snowflake and loads data from the specified table.
    """
    ctx = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )
    
    query = f"SELECT * FROM {table};"
    
    df = pd.read_sql(query, ctx)
    ctx.close()
    
    return df
