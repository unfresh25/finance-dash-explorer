import numpy as np
import yfinance as yf
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

API_KEY = os.getenv('API_KEY')

def obv_ind(df):
    df['OBV'] = np.where(df['Close'] > df['Close'].shift(1), df['Volume'], np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0)).cumsum()
    df['OBV Signal'] = df['OBV'].ewm(span=9).mean()

    return df

def macd_ind(df):
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

def stoch_ind(df, window_size=5):
    df['High-Low'] = df['High'] - df['Low']
    df['%K'] = (df['Close'] - df['Low']) / df['High-Low'] * 100
    df['%D'] = df['%K'].rolling(window=window_size).mean()
    df['Signal'] = df['%K'].ewm(span=9).mean()

    return df    

def adl_ind(df):
    df['MFM'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['ADL'] = df['MFM'] * df['Volume']
    df['A/D'] = df['ADL'].cumsum()
    df['Signal'] = df['A/D'].ewm(span=9).mean()

    return df

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="3y")
        return stock_data
    except Exception as e:
        print(f"Error al obtener la información del ticker {ticker}. {str(e)}")
        print("Obteniendo información de AAPL (Apple Inc.)...")
        return get_stock_data("AAPL")
    
@lru_cache(maxsize=32)
def get_cached_stock_data(ticker):
    return get_stock_data(ticker)

def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        address = stock_info.get('city') + ', ' + stock_info.get('state') + '.' if stock_info.get('city') and stock_info.get('state') else 'No address available'
        description = stock_info.get('longBusinessSummary') or 'No description available'
        name = stock_info.get('shortName') or 'No name available'
        website = stock_info.get('website') or 'No website available'

        max_length = 250
        if len(description) > max_length:
            last_space_index = description.rfind(' ', 0, max_length)
            description = description[:last_space_index] + "..."

        return address, description, name, website
    except Exception as e:
        print(f"Error al obtener la información del ticker {ticker}. {str(e)}")
        print("Obteniendo información de AAPL (Apple Inc.)...")
        return get_stock_info("AAPL")
    
@lru_cache(maxsize=32)
def get_cached_stock_info(ticker):
    return get_stock_info(ticker)

def get_most_active_stocks():
    df = pd.read_html("https://finance.yahoo.com/most-active?offset=0&count=100")
    return df[0]

@lru_cache(maxsize=32)
def get_cached_most_active_stocks():
    return get_most_active_stocks()
    
def get_logo(ticker):
    try:
        filename = f'{ticker}.svg'
        filepath = os.path.join('assets/stocks', filename)

        if os.path.exists(filepath):
            return filename

        url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            res = response.json()
            logo_url = res.get('results').get('branding').get('logo_url')
            
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + API_KEY
            }
            
            response = requests.request("GET", logo_url, headers=headers, data=payload)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filename
            else:
                print(f"Error al obtener el logo del ticker {ticker}. Código de estado: {response.status_code}")
                return None
        else:
            print(f"Error al obtener la información del ticker {ticker}. Código de estado: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al obtener la información del ticker {ticker}. {str(e)}")
        print("Obteniendo información de AAPL (Apple Inc.)...")
        return get_logo("AAPL")
    
@lru_cache(maxsize=32)
def get_cached_logo(ticker):
    return get_logo(ticker)


    
    