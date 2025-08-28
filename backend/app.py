from flask import Flask, jsonify
from .data_simulation import orders_df, notifications, STATUS_OPTIONS
from .ml_model import model
import random
from datetime import datetime, timedelta
import time
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   


@app.route('/orders', methods=['GET'])
def get_orders():
    df_copy = orders_df.copy()
    for col in ['ExpectedDeliveryTime', 'ActualDeliveryTime']:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].astype(str)  
    return jsonify(df_copy.to_dict(orient='records'))

@app.route('/update_status', methods=['POST'])
def update_status():
    log = None   
    for idx in range(len(orders_df)):
        row = orders_df.iloc[idx]
        if row['Status'] == 'Pending':
            orders_df.at[idx, 'Status'] = 'In-Progress'
            log = f"Retailer {row['RetailerName']}: Order {row['OrderID']} now In-Progress."
        elif row['Status'] == 'In-Progress':
            if random.random() > 0.5:
                orders_df.at[idx, 'Status'] = 'Delivered'
                actual_time = datetime.now()
                orders_df.at[idx, 'ActualDeliveryTime'] = actual_time
                log = f"Retailer {row['RetailerName']}: Order {row['OrderID']} Delivered at {actual_time.strftime('%H:%M %p')}."
    if log:   
        notifications.append(log)
    time.sleep(1)  
    return jsonify({'message': 'Statuses updated', 'notifications': notifications[-5:]})

@app.route('/analytics', methods=['GET'])
def get_analytics():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    delivered_today = orders_df[(orders_df['Status'] == 'Delivered') & (orders_df.get('ActualDeliveryTime', pd.Series()).dt.date == today)].shape[0]
    delivered_yesterday = orders_df[(orders_df['Status'] == 'Delivered') & (orders_df.get('ActualDeliveryTime', pd.Series()).dt.date == yesterday)].shape[0]
    delayed = orders_df[orders_df['Prediction'] == 'Delayed'].shape[0]
    avg_time = str((orders_df['ActualDeliveryTime'] - orders_df['ExpectedDeliveryTime']).dropna().mean()) if 'ActualDeliveryTime' in orders_df else '0'
    return jsonify({
        'delivered_today': delivered_today,
        'delivered_yesterday': delivered_yesterday,
        'delayed': delayed,
        'avg_delivery_time': avg_time
    })

if __name__ == '__main__':
    app.run(debug=True)