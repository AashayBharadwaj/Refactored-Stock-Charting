import streamlit as st
import pandas as pd
import plotly.express as px
from functions.data_fetching import fetch_stock_data  # Ensure this path is correct
from functions.ui_elements import render_header_and_text, render_layout_with_image, render_portfolio_header_and_text, render_portfolio_layout_with_image

def track_portfolio(ticker_options, default_ticker, default_start_date, default_end_date):
    render_portfolio_layout_with_image()
    render_portfolio_header_and_text()

    num_stocks = st.number_input('Number of Stocks', min_value=1, max_value=10, value=1, step=1)
    stock_details = []

    for i in range(num_stocks):
        st.subheader(f'Stock {i + 1}')
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1.5])
        
        with col1:
            stock_ticker = st.selectbox(f'Ticker for Stock {i + 1}', options=ticker_options, index=ticker_options.index(default_ticker))
        
        with col2:
            stock_start_date = st.date_input(f'Start Date for Stock {i + 1}', value=default_start_date)
        
        with col3:
            stock_end_date = st.date_input(f'End Date for Stock {i + 1}', value=default_end_date)

        with col4:
            stock_quantity = st.number_input(f'Quantity of Stock {i + 1} Purchased', min_value=1, value=1, step=1)
            
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
        
        # Diagnostic print
        # st.write("Column names in combined DataFrame:", combined_portfolio.columns.tolist())
        
        # Ensure 'Date' is a column, not an index
        if 'Date' not in combined_portfolio.columns:
            combined_portfolio.reset_index(inplace=True)
        
        # Create and display a plotly line chart for Total Investment
        fig = px.line(combined_portfolio, x='Date', y='Total Investment', title='Total Investment Over Time')
        st.plotly_chart(fig)
    else:
        st.write("No data to display.")

    return combined_portfolio
