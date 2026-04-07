import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

def generate_sample_data():
    tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "WIPRO.NS", 
               "TATAMOTORS.NS", "ITC.NS", "BAJFINANCE.NS", "SBIN.NS", "ADANIENT.NS", "^NSEI"]
    
    # 1 Year of historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    print(f"Fetching data for {len(tickers)} tickers from {start_date.date()} to {end_date.date()}...")
    
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to CSV
    csv_path = "data/india_stocks_sample.csv"
    data.to_csv(csv_path)
    print(f"Successfully saved sample data to {csv_path}")

if __name__ == "__main__":
    generate_sample_data()
