import requests
import pandas as pd

def fetch_exchange_rate_data(api_key):
    # URL to fetch historical exchange rate data from Alpha Vantage
    url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=KRW&apikey={api_key}&outputsize=full"

    response = requests.get(url)
    data = response.json()

    # Check if the API call was successful
    if "Time Series FX (Daily)" not in data:
        print("Error fetching data. Please check your API key and the API limits.")
        return

    # Parse the JSON response to extract historical data
    time_series = data["Time Series FX (Daily)"]
    dates = []
    rates = []

    for date, rate_info in time_series.items():
        dates.append(date)
        rates.append(float(rate_info["4. close"]))

    df = pd.DataFrame({
        'Timestamp': dates,
        'ExchangeRate': rates
    })

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.to_csv('../data/exchange_rates.csv', index=False)

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    api_key = 'UNQ3Q39U78AA4EED'
    fetch_exchange_rate_data(api_key)
