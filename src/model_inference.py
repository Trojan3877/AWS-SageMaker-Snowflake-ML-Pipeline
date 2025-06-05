# src/model_inference.py

import pandas as pd
import joblib
import snowflake.connector
import os

def load_model(model_path='models/fraud_detection_model.joblib'):
    model = joblib.load(model_path)
    return model

def predict(model, input_data):
    predictions = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)[:,1]  # Probability of fraud
    return predictions, prediction_proba

def write_predictions_to_snowflake(transaction_ids, predictions, probabilities):
    """
    Writes predictions back to Snowflake as a new table or updates an existing one.
    """
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE OR REPLACE TABLE fraud_predictions (
            transaction_id INT,
            is_fraud_predicted BOOLEAN,
            fraud_probability FLOAT
        );
    """)
    
    # Insert predictions row by row
    insert_sql = """
        INSERT INTO fraud_predictions (transaction_id, is_fraud_predicted, fraud_probability)
        VALUES (%s, %s, %s)
    """
    
    for tx_id, pred, proba in zip(transaction_ids, predictions, probabilities):
        cursor.execute(insert_sql, (tx_id, bool(pred), float(proba)))
    
    conn.commit()
    conn.close()
