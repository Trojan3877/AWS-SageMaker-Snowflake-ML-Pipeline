# tests/test_feature_engineering.py

import pytest
import pandas as pd
from src.feature_engineering import preprocess_data


def test_preprocess_fills_missing_amounts():
    """
    Ensure missing 'amount' values are filled with the column median.
    """
    df = pd.DataFrame({
        'amount': [100.0, None, 50.0],
        'transaction_type': ['purchase', 'transfer', 'purchase'],
        'is_fraud': [0, 1, 0]
    })
    result = preprocess_data(df.copy())
    assert result['amount'].isna().sum() == 0


def test_preprocess_encodes_transaction_type():
    """
    Ensure categorical 'transaction_type' column is one-hot encoded.
    """
    df = pd.DataFrame({
        'amount': [100.0, 200.0, 300.0],
        'transaction_type': ['purchase', 'transfer', 'cash_withdrawal'],
        'is_fraud': [0, 1, 0]
    })
    result = preprocess_data(df.copy())
    assert 'transaction_type' not in result.columns
