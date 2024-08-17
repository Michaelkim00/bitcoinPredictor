from flask import Flask, render_template, request, jsonify
import pandas as pd
from joblib import load
import numpy as np
import datetime

app = Flask(__name__)

# Load the trained model and scaler
model = load('models/exchange_rate_predictor.joblib')
scaler = load('models/scaler.joblib')

# Load the actual data
df = pd.read_csv('data/exchange_rates.csv', parse_dates=['Timestamp'], index_col='Timestamp')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    date_str = request.form['timestamp']  # Get date from form
    clicked_date = pd.to_datetime(date_str)  # Convert date string to datetime object
    current_date = datetime.datetime.now()  # Get current date

    # Generate prediction range from current date to clicked date
    prediction_range = pd.date_range(start=current_date, end=clicked_date, freq='D')

    # Convert timestamps to milliseconds
    prediction_timestamps_ms = [int(ts.timestamp() * 1000) for ts in prediction_range]

    # Scale the input timestamps
    scaled_timestamps = scaler.transform(np.array(prediction_timestamps_ms).reshape(-1, 1))

    # Make predictions
    predicted_prices_line = model.predict(scaled_timestamps)

    # Fetch actual data points up to the clicked date
    actual_data = df.loc[df.index <= clicked_date]
    actual_timestamps = actual_data.index.strftime('%Y-%m-%d').tolist()
    actual_prices = actual_data['ExchangeRate'].tolist()

    return jsonify({
        'predicted_prices_line': predicted_prices_line.tolist(),
        'timestamps_line': prediction_range.strftime('%Y-%m-%d').tolist(),
        'actual_prices': actual_prices,
        'timestamps': actual_timestamps,
        'predicted_price': predicted_prices_line[-1]  # The last prediction
    })

if __name__ == '__main__':
    app.run(debug=True)
