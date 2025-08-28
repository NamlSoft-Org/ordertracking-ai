import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from backend.data_simulation import orders_df

def train_model():
    
    num_samples = 1000
    data = {
        'Distance': np.random.uniform(5, 50, num_samples),
        'Quantity': np.random.randint(10, 100, num_samples),
        'DeliveryBoyLoad': np.random.randint(1, 10, num_samples),
        'TrafficDelay': np.random.uniform(0, 2, num_samples),
    }
    df = pd.DataFrame(data)
    df['Label'] = np.where(
        (df['Distance'] > 30) | (df['TrafficDelay'] > 1) | (df['DeliveryBoyLoad'] > 7),
        'Delayed', 'On-Time'
    )

    X = df[['Distance', 'Quantity', 'DeliveryBoyLoad', 'TrafficDelay']]
    y = df['Label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    
    orders_features = orders_df[['Distance', 'Quantity', 'DeliveryBoyLoad', 'TrafficDelay']]
    orders_df['Prediction'] = model.predict(orders_features)
    return model

model = train_model()
