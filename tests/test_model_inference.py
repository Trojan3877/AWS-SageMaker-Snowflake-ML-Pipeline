# tests/test_model_inference.py

import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock
from src import model_inference


def test_predict_output():
    """
    Smoke-test: create a mock model and verify predict returns correct shape.
    """
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([0, 1])
    mock_model.predict_proba.return_value = np.array([[0.9, 0.1], [0.2, 0.8]])

    test_input = pd.DataFrame(
        [[100.0, 0.2, 1, 0, 0]],
        columns=[
            'amount', 'feature2',
            'transaction_type_purchase',
            'transaction_type_transfer',
            'transaction_type_cash_withdrawal'
        ]
    )

    preds, probas = model_inference.predict(mock_model, test_input)
    assert preds is not None
    assert probas is not None
