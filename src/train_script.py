# src/train_script.py

import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import joblib
import os

if __name__ == "__main__":
    # Load training data
    train_data = pd.read_csv(os.path.join('/opt/ml/input/data/train', 'train.csv'))
    target_column = 'is_fraud'

    X_train = train_data.drop(columns=[target_column])
    y_train = train_data[target_column]

    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    output_dir = os.path.join('/opt/ml/model')
    joblib.dump(model, os.path.join(output_dir, 'model.joblib'))
