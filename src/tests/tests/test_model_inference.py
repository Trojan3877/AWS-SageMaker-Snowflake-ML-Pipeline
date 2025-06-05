# tests/test_model_inference.py

import pytest
from src import model_inference
import pandas as pd

def test_model_loading():
    model = model_inference.load_model('models/fraud_detection_model.joblib')
    assert model is not None

def test_predict_output():
    model = model_inference.load_model('models/fraud_detection_model.joblib')

    # Example input → adjust to match your trained feature columns
    test_input = pd.DataFrame([[100.0, 0.2, 1, 0, 0]], 
                              columns=['amount', 'feature2', 'transaction_type_purchase', 'transaction_type_transfer', 'transaction_type_cash_withdrawal'])

    preds, probas = model_inference.predict(model, test_input)

    assert len(preds) == len(test_input)
    assert len(probas) == len(test_input)
    assert all(0.0 <= p <= 1.0 for p in probas)
