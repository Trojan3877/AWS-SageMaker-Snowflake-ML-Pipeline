# processing/job.py
"""
SageMaker Processing Job — Feature Engineering
-----------------------------------------------
Pulls raw transactions from Snowflake, applies feature engineering,
and writes processed data back to S3 for model training.
"""

import argparse
import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()


def load_raw_data():
    """Load raw transaction data from Snowflake."""
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA'),
    )
    query = "SELECT * FROM raw_transactions;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def engineer_features(df):
    """Apply feature engineering transformations."""
    df['amount'] = df['transaction_amount'].fillna(df['transaction_amount'].median())
    df['is_foreign'] = df['is_foreign_transaction'].astype(int)
    df['card_present_flag'] = df['card_present'].astype(int)
    df = pd.get_dummies(df, columns=['transaction_category'], drop_first=True)
    drop_cols = [
        'transaction_id', 'account_id', 'merchant_id',
        'transaction_date', 'device_id', 'ip_address',
        'transaction_amount', 'is_foreign_transaction', 'card_present',
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=str, default='/opt/ml/processing/output')
    args = parser.parse_args()

    df_raw = load_raw_data()
    df_processed = engineer_features(df_raw)

    os.makedirs(args.output_dir, exist_ok=True)
    output_path = os.path.join(args.output_dir, 'processed_data.csv')
    df_processed.to_csv(output_path, index=False)
    print(f"Processed data written to {output_path}")
