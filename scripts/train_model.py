import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from joblib import dump

# Load the data
df = pd.read_csv('../data/exchange_rates.csv', parse_dates=['Timestamp'])

# Convert timestamps to milliseconds since epoch
df['Timestamp_ms'] = df['Timestamp'].astype('int64') // 10**6

# Feature and target
X = df[['Timestamp_ms']]
y = df['ExchangeRate']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the model
model = LinearRegression()
model.fit(X_scaled, y)

# Save the model and scaler
dump(model, '../models/exchange_rate_predictor.joblib')
dump(scaler, '../models/scaler.joblib')
