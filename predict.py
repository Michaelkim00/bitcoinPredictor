from flask import Flask, render_template, request, jsonify
import pandas as pd
from joblib import load
import numpy as np

app = Flask(__name__)

# Load the trained model and scaler
model = load('models/exchange_rate_predictor.joblib')
scaler = load('models/scaler.joblib')

# Load the actual data (assuming you have it stored in a CSV file)
df = pd.read_csv('data/exchange_rates.csv', parse_dates=['Timestamp'], index_col='Timestamp')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    timestamp = pd.to_datetime(request.form['timestamp'])
    timestamp_ms = int(timestamp.timestamp() * 1000)  # Convert timestamp to milliseconds

    # Scale the input as done during training
    scaled_timestamp = scaler.transform(np.array([[timestamp_ms]]))

    # Make prediction
    prediction = model.predict(scaled_timestamp)[0]

    # Fetch actual data points for the prediction
    actual_data = df.loc[df.index <= timestamp]
    timestamps = actual_data.index.strftime('%Y-%m-%d').tolist()
    actual_prices = actual_data['ExchangeRate'].tolist()

    # Generate prediction line data
    timestamps_line = pd.date_range(start=timestamp, periods=100, freq='D')
    predicted_prices_line = model.predict(scaler.transform([[int(ts.timestamp() * 1000)] for ts in timestamps_line]))

    return jsonify({
        'predicted_price': prediction,
        'timestamps': timestamps,
        'actual_prices': actual_prices,
        'timestamps_line': timestamps_line.strftime('%Y-%m-%d').tolist(),
        'predicted_prices_line': predicted_prices_line.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)
