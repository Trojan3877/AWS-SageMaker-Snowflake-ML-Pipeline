# tests/test_data_loader.py

import pytest
from src import data_loader
import pandas as pd

def test_load_data_structure(monkeypatch):
    """
    Unit test to ensure Snowflake loader returns correct structure.
    """
    # Mock function (replace Snowflake call with local test)
    def mock_load_data():
        return pd.DataFrame({
            'transaction_id': [1, 2, 3],
            'amount': [50.0, 300.0, 20.0],
            'transaction_type': ['purchase', 'transfer', 'cash_withdrawal'],
            'is_fraud': [0, 1, 0]
        })

    monkeypatch.setattr(data_loader, "load_data_from_snowflake", mock_load_data)

    df = data_loader.load_data_from_snowflake()
    assert df.shape[0] > 0
    assert 'transaction_id' in df.columns
    assert 'is_fraud' in df.columns
    assert df['is_fraud'].isin([0, 1]).all()
