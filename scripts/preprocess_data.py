import pandas as pd

def preprocess_data(filepath):
    df = pd.read_csv(filepath)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    return df

if __name__ == "__main__":
    df = preprocess_data('../data/exchange_rates.csv')
    print(df.head())
