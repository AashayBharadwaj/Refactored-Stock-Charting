import streamlit as st
import pandas as pd
from datetime import datetime
from functions.ui_elements import render_header_and_text, render_layout_with_image,render_portfolio_header_and_text, render_portfolio_layout_with_image
from functions.data_fetching import get_ticker_options, fetch_stock_data
from functions.data_processing import process_data_and_metrics,process_price_data, plot_dual_y_axes, calculate_annual_return, calculate_standard_deviation, calculate_risk_adjusted_return, default_ticker, default_ticker_2,default_start_date, default_end_date


# Get ticker options
ticker_options = get_ticker_options()


# Sidebar options
sidebar_option = st.sidebar.radio('Select an Option', ['Track Stock Performance', 'Track Portfolio'])


if sidebar_option == 'Track Stock Performance':
    st.sidebar.header('Track Stock Performance')

    # Call the function to render layout with image
    render_layout_with_image()

# Call the cached function to render header and text
    render_header_and_text()

    # User inputs with default values
    st.sidebar.header('Select your first stock')
    ticker = st.sidebar.selectbox('Stock Ticker', options=ticker_options, index=ticker_options.index(default_ticker))
    start_date = st.sidebar.date_input('Start Date', value=default_start_date)
    end_date = st.sidebar.date_input('End Date', value=default_end_date)
    
    compare_stock = st.sidebar.checkbox('Compare with another stock')
    if compare_stock:
        ticker_2 = st.sidebar.selectbox('Stock Ticker', options=ticker_options, index=ticker_options.index(default_ticker_2))
    else:
        ticker_2 = 'No Selection'

    # Fetch stock data for the first ticker
    data = fetch_stock_data(ticker, start_date, end_date)

    # Check if the second ticker is selected and fetch data if it is
    if ticker_2 != 'No Selection':
        data_2 = fetch_stock_data(ticker_2, start_date, end_date)
        # Plot stock data with dual y-axes
        fig = plot_dual_y_axes(data, ticker, data_2, ticker_2)
        explanation = f'This is how {ticker} has performed against {ticker_2} in the selected time period!'
    else:
        # Plot stock data for the first ticker only
        fig = process_price_data(data, ticker)
        explanation = f'This is how {ticker} has performed in the selected time period!'

    # Display the plot
    st.plotly_chart(fig)
    st.subheader(explanation)

    # Process data and metrics for detailed view
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

    # Optionally show detailed data
    show_data_checkbox = st.checkbox('Show Detailed Data')
    if show_data_checkbox:
        st.write(data2)
        
elif sidebar_option == 'Track Portfolio':
    
# Call the function to render layout with image
    render_portfolio_layout_with_image()

# Call the cached function to render header and text
    render_portfolio_header_and_text()
    
# Input number of stocks the user wants to track
    num_stocks = st.number_input('Number of Stocks', min_value=1, max_value=10, value=1, step=1)

    # Initialize an empty list to store stock data
    portfolio_dataframes = []
    stock_quantities = []
    
# Collect data for each stock
    for i in range(num_stocks):
        st.subheader(f'Stock {i + 1}')
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        
        # Input for stock ticker
        with col1:
            stock_ticker = st.selectbox(f'Ticker for Stock {i + 1}', options=ticker_options, index=ticker_options.index(default_ticker))
        
        # Input for start date
        with col2:
            stock_start_date = st.date_input(f'Date of Purchase for Stock {i + 1}', value=default_start_date)
        
        # Input for end date
        with col3:
            stock_end_date = st.date_input(f'End Date for Stock {i + 1}', value=default_end_date)

        # Input for quantity of stocks purchased
        with col4:
            stock_quantity = st.number_input(f'Quantity of Stock {i + 1} Purchased', min_value=1, value=1, step=1)

        # Fetch stock data for the current stock
        stock_data = fetch_stock_data(stock_ticker, stock_start_date, stock_end_date)
        portfolio_dataframes.append(stock_data)


    # Display portfolio data for confirmation
    if st.button('Show Portfolio Data'):
        for i, df in enumerate(portfolio_dataframes):
            st.subheader(f"Stock {i + 1}: Data")
            st.write(df)
    
   
    
    # Calculate invested amount for each stock
    invested_amounts = []
    for df in portfolio_dataframes:
        # Get the closing price on the purchase date
        purchase_date = df.index.min()
        closing_price = df.loc[purchase_date]['Close']
        
        # Calculate invested amount
        invested_amount = stock_quantity * closing_price
        invested_amounts.append(invested_amount)

    # Create a DataFrame for portfolio performance
    portfolio_performance = pd.DataFrame({
        'Date': portfolio_dataframes[0].index,
        'Portfolio Value': 0  # Initialize with zeros
    })

    # Calculate cumulative portfolio value
    for i, df in enumerate(portfolio_dataframes):
        portfolio_performance['Portfolio Value'] += df['Close'] * stock_quantity

    # Display portfolio performance DataFrame
    st.write('Portfolio Performance:')
    st.write(portfolio_performance)
 
#################33


# # Call the function to render layout with image
#     render_portfolio_layout_with_image()

# # Call the cached function to render header and text
#     render_portfolio_header_and_text()
    
# # Input number of stocks the user wants to track
#     num_stocks = st.number_input('Number of Stocks', min_value=1, max_value=10, value=1, step=1)

#     # Initialize an empty list to store stock data
#     portfolio_dataframes = []
#     stock_quantities = []
    
# # Collect data for each stock
#     for i in range(num_stocks):
#         st.subheader(f'Stock {i + 1}')
#         col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        
#         # Input for stock ticker
#         with col1:
#             stock_ticker = st.selectbox(f'Ticker for Stock {i + 1}', options=ticker_options, index=ticker_options.index(default_ticker))
        
#         # Input for start date
#         with col2:
#             stock_start_date = st.date_input(f'Date of Purchase for Stock {i + 1}', value=default_start_date)
        
#         # Input for end date
#         with col3:
#             stock_end_date = st.date_input(f'End Date for Stock {i + 1}', value=default_end_date)

#         # Input for quantity of stocks purchased
#         with col4:
#             stock_quantity = st.number_input(f'Quantity of Stock {i + 1} Purchased', min_value=1, value=1, step=1)
            
#         # Fetch stock data for the current stock
#         stock_data = fetch_stock_data(stock_ticker, stock_start_date, stock_end_date)
#         portfolio_dataframes.append(stock_data)
#         stock_quantities.append(stock_quantity)  # Store the quantity for later calculations
#         st.write(f"Data for {stock_ticker} from {stock_start_date} to {stock_end_date}:")
#         st.dataframe(stock_data)  # Display the dataframe in Streamlit