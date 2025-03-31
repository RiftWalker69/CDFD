from django.db import models
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

class FraudModel:
    def __init__(self):
        try:
            artifacts = joblib.load('fraud_detector.joblib')
            self.model = artifacts['model']
            self.features = artifacts['features']
            self.threshold = artifacts['threshold']
        except Exception as e:
            raise ValueError(f"Model loading failed: {str(e)}")

    def predict(self, transaction_data):
        try:
            # Convert to DataFrame
            X = pd.DataFrame([transaction_data])
            
            # Feature engineering
            X['transaction_speed'] = X['distance_from_last_transaction'] / (X['distance_from_home'] + 0.001)
            
            # Validate features
            missing = [f for f in self.features if f not in X.columns]
            if missing:
                raise ValueError(f'Missing features: {missing}')
            
            # Predict
            proba = self.model.predict_proba(X[self.features])[0,1]
            return {
                'is_fraud': bool(proba >= self.threshold),
                'probability': float(proba),
                'threshold': float(self.threshold)
            }
        except Exception as e:
            raise ValueError(str(e))

class Transaction(models.Model):
    distance_from_home = models.FloatField()
    distance_from_last_transaction = models.FloatField()
    ratio_to_median_purchase_price = models.FloatField()
    used_chip = models.BooleanField()
    online_order = models.BooleanField()
    is_fraud = models.BooleanField()
    probability = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']