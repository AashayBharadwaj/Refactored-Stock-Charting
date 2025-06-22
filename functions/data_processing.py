import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .data_fetching import fetch_stock_data
# from app import ticker,start_date,end_date




def process_price_data(data, ticker):
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
    fig.update_yaxes(title_text=f"{ticker} Price")
    return fig


# Default values
default_ticker = 'MSFT'
default_ticker_2 = 'No Selection'
today = datetime.today()
default_end_date = today

# Get the most recent Monday before today
last_monday = today - timedelta(days=today.weekday() + 7)
default_start_date = last_monday

def calculate_annual_return(data):
    return data['% Change'].mean() * 252 * 100

def calculate_standard_deviation(data):
    return np.std(data['% Change']) * np.sqrt(252) * 100

def calculate_risk_adjusted_return(annual_return, stdev):
    return annual_return / stdev

# Function to create a plot with two y-axes
def plot_dual_y_axes(data1, ticker1, data2=None, ticker2=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for the first ticker
    fig.add_trace(
        go.Scatter(x=data1.index, y=data1['Adj Close'], name=ticker1, line=dict(color='#615EFC')),
        secondary_y=False,
    )

    # Add traces for the second ticker, if provided
    if data2 is not None and ticker2 is not None:
        fig.add_trace(
            go.Scatter(x=data2.index, y=data2['Adj Close'], name=ticker2, line=dict(color='#ACD793')),
            secondary_y=True,
        )

    # Add figure title
    fig.update_layout(
        title_text="Stock Price Data"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles with just the ticker name followed by "Price"
    fig.update_yaxes(title_text=f"{ticker1} Price", secondary_y=False)
    fig.update_yaxes(title_text=f"{ticker2} Price", secondary_y=True)

    return fig



# # # Fetch stock data
# data = fetch_stock_data(ticker, start_date, end_date)


def process_data_and_metrics(data):
    data2 = data.copy()
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)

    annual_return = calculate_annual_return(data2)
    stdev = calculate_standard_deviation(data2)
    risk_adj_return = calculate_risk_adjusted_return(annual_return, stdev)

    # Round values to two decimal places
    annual_return_rounded = round(annual_return, 2)
    stdev_rounded = round(stdev, 2)
    risk_adj_return_rounded = round(risk_adj_return, 2)

    # Display the rounded values
    st.write('Annual Return is ', annual_return_rounded, '%')
    st.write('Risk Adj Return is', risk_adj_return_rounded, '%')
    
    return data2, annual_return_rounded, stdev_rounded, risk_adj_return_rounded


#####################

# def track_stock_performance(ticker, start_date, end_date, ticker_2='No Selection'):
#     # Fetch stock data for the first ticker
#     data = fetch_stock_data(ticker, start_date, end_date)

#     if ticker_2 != 'No Selection':
#         # Fetch stock data for the second ticker if selected
#         data_2 = fetch_stock_data(ticker_2, start_date, end_date)
#         # Plot stock data with dual y-axes
#         fig = plot_dual_y_axes(data, ticker, data_2, ticker_2)
#         explanation = f'This is how {ticker} has performed against {ticker_2} in the selected time period!'
#     else:
#         # Plot stock data for the first ticker only
#         fig = process_price_data(data, ticker)
#         explanation = f'This is how {ticker} has performed in the selected time period!'

#     # Display the plot
#     st.plotly_chart(fig)
#     st.subheader(explanation)