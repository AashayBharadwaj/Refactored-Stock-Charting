import streamlit as st
import pandas as pd
import plotly.express as px
from functions.data_fetching import fetch_stock_data
from functions.ui_elements import render_header_and_text, render_layout_with_image, render_portfolio_header_and_text, render_portfolio_layout_with_image

def track_portfolio(ticker_options, default_ticker, default_start_date, default_end_date):
    render_portfolio_layout_with_image()
    render_portfolio_header_and_text()

    num_stocks = st.number_input('Number of Stocks', min_value=1, max_value=10, value=1, step=1)
    
    # Create a dataframe to hold the user inputs
    stock_inputs = pd.DataFrame({
        'Stock Number': [i + 1 for i in range(num_stocks)],
        'Ticker': [default_ticker] * num_stocks,
        'Start Date': [default_start_date] * num_stocks,
        'End Date': [default_end_date] * num_stocks,
        'Quantity': [1] * num_stocks
    })

    # Display the input table
    st.markdown("### Enter Stock Details")
    for i in range(num_stocks):
        cols = st.columns([1, 2, 2, 2, 2])
        cols[0].markdown(f"**Stock {i + 1}**")
        stock_inputs.at[i, 'Ticker'] = cols[1].selectbox(f'Select Ticker {i + 1}', options=ticker_options, index=ticker_options.index(default_ticker), key=f'ticker_{i}')
        stock_inputs.at[i, 'Start Date'] = cols[2].date_input(f'Start Date {i + 1}', value=default_start_date, key=f'start_date_{i}')
        stock_inputs.at[i, 'End Date'] = cols[3].date_input(f'End Date {i + 1}', value=default_end_date, key=f'end_date_{i}')
        stock_inputs.at[i, 'Quantity'] = cols[4].number_input(f'Quantity {i + 1}', min_value=1, value=1, step=1, key=f'quantity_{i}')

    st.write(stock_inputs)  # Display the user input table for review
    
    stock_details = []

    for i in range(num_stocks):
        stock_ticker = stock_inputs.at[i, 'Ticker']
        stock_start_date = stock_inputs.at[i, 'Start Date']
        stock_end_date = stock_inputs.at[i, 'End Date']
        stock_quantity = stock_inputs.at[i, 'Quantity']
        
        stock_data = fetch_stock_data(stock_ticker, stock_start_date, stock_end_date)
        stock_data['Quantity'] = stock_quantity
        stock_data[f'{stock_ticker} Invested'] = stock_data['Close'] * stock_quantity
        
        stock_data = stock_data[['Close', 'Quantity', f'{stock_ticker} Invested']].rename(columns={'Close': f'{stock_ticker} Close'})
        stock_details.append(stock_data)

    if stock_details:
        from functools import reduce
        combined_portfolio = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), stock_details)
        combined_portfolio.fillna(0, inplace=True)
        combined_portfolio['Total Investment'] = combined_portfolio[[col for col in combined_portfolio.columns if 'Invested' in col]].sum(axis=1)
        
        # Ensure 'Date' is a column, not an index
        if 'Date' not in combined_portfolio.columns:
            combined_portfolio.reset_index(inplace=True)
        
        # Create and display a plotly line chart for Total Investment
        fig = px.line(combined_portfolio, x='Date', y='Total Investment', title='Total Investment Over Time')
        st.plotly_chart(fig)
    else:
        st.write("No data to display.")

    return combined_portfolio

# Call the function with sample data (replace with your actual data fetching and processing logic)
ticker_options = ['MSFT', 'AAPL', 'GOOGL']
default_ticker = 'MSFT'
default_start_date = pd.to_datetime('2020-01-01')
default_end_date = pd.to_datetime('2024-07-04')
track_portfolio(ticker_options, default_ticker, default_start_date, default_end_date)
