# tests/test_model_inference.py

import pytest
from src import model_inference
import pandas as pd

def test_model_loading():
    model = model_inference.load_model(model_path='models/fraud_detection_model.joblib')
    assert model is not None

def test_prediction_shape():
    model = model_inference.load_model(model_path='models/fraud_detection_model.joblib')
    
    # Example test input → adjust as per your feature columns
    input_data = pd.DataFrame([[100.0, 0.5, 0, 1, 0]], columns=['amount', 'feature2', 'transaction_type_A', 'transaction_type_B', 'transaction_type_C'])
    
    preds = model_inference.predict(model, input_data)
    assert len(preds) == len(input_data)
