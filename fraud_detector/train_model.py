import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Generate sample data
np.random.seed(42)
n_samples = 1000

# Generate features
data = {
    'distance_from_home': np.random.uniform(0, 100, n_samples),
    'distance_from_last_transaction': np.random.uniform(0, 50, n_samples),
    'ratio_to_median_purchase_price': np.random.uniform(0.1, 5, n_samples),
    'used_chip': np.random.randint(0, 2, n_samples),
    'online_order': np.random.randint(0, 2, n_samples)
}

# Create DataFrame
df = pd.DataFrame(data)

# Create target variable (fraud) based on some rules
df['is_fraud'] = (
    (df['distance_from_home'] > 80) |  # Very far from home
    (df['ratio_to_median_purchase_price'] > 3) |  # Very high purchase amount
    (df['online_order'] & (df['distance_from_last_transaction'] > 30))  # Online order with large distance from last transaction
).astype(int)

# Feature engineering
df['transaction_speed'] = df['distance_from_last_transaction'] / (df['distance_from_home'] + 0.001)

# Prepare features for training
features = [
    'distance_from_home',
    'distance_from_last_transaction',
    'ratio_to_median_purchase_price',
    'used_chip',
    'online_order',
    'transaction_speed'
]

X = df[features]
y = df['is_fraud']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model artifacts
artifacts = {
    'model': model,
    'features': features,
    'threshold': 0.5  # Decision threshold
}

joblib.dump(artifacts, 'fraud_detector.joblib')
print("Model saved successfully!") 