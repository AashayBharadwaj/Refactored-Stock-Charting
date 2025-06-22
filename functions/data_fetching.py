import pandas as pd
import requests
# import yfinance as yf
from config import POLYGON_API_KEY 


def get_ticker_options():
    ticker_data = pd.read_csv('Stock-Tickers.csv')
    return ticker_data['Tickers'].tolist()

# def fetch_stock_data(ticker, start_date, end_date):
#     dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days only
#     rows = []

#     for date in dates:
#         date_str = date.strftime('%Y-%m-%d')
#         url = f"https://api.polygon.io/v1/open-close/{ticker}/{date_str}?adjusted=true&apiKey={POLYGON_API_KEY}"
#         r = requests.get(url)
#         if r.status_code == 200:
#             result = r.json()
#             if result.get("status") == "OK":
#                 rows.append({
#                     "Date": pd.to_datetime(result['from']),
#                     "Close": result['close']
#                 })

#     df = pd.DataFrame(rows)
#     df.set_index("Date", inplace=True)
#     df.rename(columns={"Close": "Adj Close"}, inplace=True)  # For compatibility with existing logic
#     return df

    
def fetch_stock_data(ticker, start_date, end_date):
    start = pd.to_datetime(start_date).strftime("%Y-%m-%d")
    end = pd.to_datetime(end_date).strftime("%Y-%m-%d")

    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/"
        f"{start}/{end}?adjusted=true&sort=asc&apiKey={POLYGON_API_KEY}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Polygon API error: {response.status_code} - {response.text}")

    data = response.json()
    if 'results' not in data:
        raise Exception("No results returned by Polygon API.")

    df = pd.DataFrame(data['results'])
    df['Date'] = pd.to_datetime(df['t'], unit='ms')
    df['Adj Close'] = df['c']

    return df[['Date', 'Adj Close']]