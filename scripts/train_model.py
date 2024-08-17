import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from joblib import dump

# Load the data
df = pd.read_csv('../data/exchange_rates.csv', parse_dates=['Timestamp'])

# Convert timestamps to milliseconds since epoch
df['Timestamp_ms'] = df['Timestamp'].astype('int64') // 10**6

# Feature and target
X = df[['Timestamp_ms']]
y = df['ExchangeRate']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)

# Calculate metrics
mae_train = mean_absolute_error(y_train, y_pred_train)
mse_train = mean_squared_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
mse_test = mean_squared_error(y_test, y_pred_test)

print(f"Training MAE: {mae_train}, MSE: {mse_train}")
print(f"Testing MAE: {mae_test}, MSE: {mse_test}")

# Save the model and scaler
dump(model, '../models/exchange_rate_predictor.joblib')
dump(scaler, '../models/scaler.joblib')
