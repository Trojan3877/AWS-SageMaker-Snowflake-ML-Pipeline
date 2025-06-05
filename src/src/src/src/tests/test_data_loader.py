# tests/test_data_loader.py

import pytest
from src import data_loader

def test_load_data_structure(monkeypatch):
    # Mock function for unit test (replace actual connection)
    def mock_load_data(*args, **kwargs):
        import pandas as pd
        return pd.DataFrame({'transaction_id': [1, 2], 'amount': [100.0, 250.0], 'is_fraud': [0, 1]})
    
    monkeypatch.setattr(data_loader, "load_data_from_snowflake", mock_load_data)
    
    df = data_loader.load_data_from_snowflake("","","","","","","")
    assert df.shape[0] > 0
    assert 'is_fraud' in df.columns
