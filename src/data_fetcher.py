"""
Data fetcher module for BIST 100 analysis
Fetches data from Yahoo Finance and FRED API
"""

import yfinance as yf
import pandas as pd
from fredapi import Fred
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DataFetcher:
    def __init__(self, start_date='2010-01-01', end_date=None):
        """
        Initialize DataFetcher
        
        Args:
            start_date (str): Start date for data fetching (YYYY-MM-DD)
            end_date (str): End date for data fetching (YYYY-MM-DD), defaults to today
        """
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.today().strftime('%Y-%m-%d')
        self.fred_api_key = os.getenv('FRED_API_KEY')
        
    def fetch_bist100(self):
        """Fetch BIST 100 data from Yahoo Finance"""
        print("Fetching BIST 100 data...")
        bist = yf.download('XU100.IS', start=self.start_date, end=self.end_date, progress=False)
        # Eğer MultiIndex ise düzelt
        if isinstance(bist.columns, pd.MultiIndex):
            bist = bist['Adj Close'].iloc[:, 0] if 'Adj Close' in bist.columns.get_level_values(0) else bist['Close'].iloc[:, 0]
        else:
            bist = bist['Adj Close'] if 'Adj Close' in bist.columns else bist['Close']
        return bist
    
    def fetch_usdtry(self):
        """Fetch USD/TRY exchange rate from Yahoo Finance"""
        print("Fetching USD/TRY data...")
        usdtry = yf.download('USDTRY=X', start=self.start_date, end=self.end_date, progress=False)
        # Eğer MultiIndex ise düzelt
        if isinstance(usdtry.columns, pd.MultiIndex):
            usdtry = usdtry['Adj Close'].iloc[:, 0] if 'Adj Close' in usdtry.columns.get_level_values(0) else usdtry['Close'].iloc[:, 0]
        else:
            usdtry = usdtry['Adj Close'] if 'Adj Close' in usdtry.columns else usdtry['Close']
        return usdtry
    
    def fetch_us_cpi(self):
        """Fetch US CPI data from FRED API"""
        print("Fetching US CPI data...")
        if not self.fred_api_key:
            raise ValueError("FRED_API_KEY not found in environment variables")
        
        fred = Fred(api_key=self.fred_api_key)
        cpi = fred.get_series('CPIAUCSL', observation_start=self.start_date, observation_end=self.end_date)
        return cpi
    
    def fetch_all_data(self):
        """Fetch all required data and return as a combined DataFrame"""
        bist = self.fetch_bist100()
        usdtry = self.fetch_usdtry()
        cpi = self.fetch_us_cpi()
        
        # Combine all data
        df = pd.DataFrame({
            'BIST_TRY': bist,
            'USDTRY': usdtry
        })
        
        # Resample CPI to daily and forward fill
        cpi_daily = cpi.resample('D').ffill()
        df['CPI'] = cpi_daily
        
        # Forward fill missing values
        df = df.ffill()
        
        # Calculate USD-adjusted BIST
        df['BIST_USD'] = df['BIST_TRY'] / df['USDTRY']
        
        # Calculate inflation-adjusted BIST (base = first value)
        cpi_base = df['CPI'].iloc[0]
        df['BIST_USD_Real'] = df['BIST_USD'] / (df['CPI'] / cpi_base)
        
        print(f"Data fetched successfully! Shape: {df.shape}")
        return df
    
    def save_data(self, df, filename='bist_analysis_data.csv'):
        """Save DataFrame to CSV"""
        filepath = os.path.join('data', filename)
        df.to_csv(filepath)
        print(f"Data saved to {filepath}")

if __name__ == "__main__":
    # Test the fetcher
    fetcher = DataFetcher(start_date='2010-01-01')
    df = fetcher.fetch_all_data()
    fetcher.save_data(df)
    print(df.head())
    print(df.tail())