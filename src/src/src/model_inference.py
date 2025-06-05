# src/model_inference.py

"""
Model Inference Module
----------------------
Loads trained model and performs predictions.
"""

import joblib
import pandas as pd

def load_model(model_path='models/fraud_detection_model.joblib'):
    """
    Loads the trained model from disk.
    """
    model = joblib.load(model_path)
    return model

def predict(model, input_data):
    """
    Performs inference using the trained model.
    """
    predictions = model.predict(input_data)
    return predictions
