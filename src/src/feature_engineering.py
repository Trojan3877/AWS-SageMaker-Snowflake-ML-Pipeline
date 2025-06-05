# src/feature_engineering.py

"""
Feature Engineering Module
--------------------------
Performs cleaning and feature engineering for fraud detection model.
"""

import pandas as pd

def preprocess_data(df):
    """
    Preprocess the data:
    - Handle missing values
    - Encode categorical variables
    - Normalize numerical features
    """
    # Example: fill missing amounts with median
    df['amount'].fillna(df['amount'].median(), inplace=True)
    
    # Example: encode transaction type (categorical)
    df = pd.get_dummies(df, columns=['transaction_type'], drop_first=True)
    
    # More feature engineering can be added here
    
    return df
