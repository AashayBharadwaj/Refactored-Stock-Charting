import streamlit as st
import pandas as pd
from datetime import datetime
from functions.ui_elements import render_header_and_text, render_layout_with_image,render_portfolio_header_and_text, render_portfolio_layout_with_image
from functions.data_fetching import get_ticker_options, fetch_stock_data
from functions.data_processing import process_data_and_metrics,process_price_data, plot_dual_y_axes, calculate_annual_return, calculate_standard_deviation, calculate_risk_adjusted_return, default_ticker, default_ticker_2,default_start_date, default_end_date
from functions.portfolio_new import track_portfolio

# Get ticker options
ticker_options = get_ticker_options()

# Title for the sidebar
st.sidebar.title('Menu')

st.sidebar.markdown('Select the functionality you want to use:')

# Sidebar options with enhanced styling
sidebar_option = st.sidebar.radio('', ['Track Stock Performance', 'Track Portfolio'], index=0)

st.sidebar.markdown('---')  # Adding a separator line


# Sidebar options
# sidebar_option = st.sidebar.radio('Select an Option', ['Track Stock Performance', 'Track Portfolio'])


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
    compare_sandp = st.sidebar.checkbox('Compare with S&P 500')
    
    if compare_stock:
        ticker_2 = st.sidebar.selectbox('Stock Ticker', options=ticker_options, index=ticker_options.index(default_ticker_2))
    else:
        ticker_2 = 'No Selection'

    if compare_sandp:
        ticker_3 = '^GSPC'
    else:
        ticker_3 = 'No selection'
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
        if compare_sandp:
            # ticker_2 = 'No Selection'
            data_3=fetch_stock_data(ticker_3,start_date,end_date)
            fig = plot_dual_y_axes(data,ticker,data_3,ticker_3)
            explanation = f'This is how {ticker} has performed against S&P 500 in the selected time period!'
        else:    
            fig = process_price_data(data, ticker)
                # Calculate the return on $1000 invested on the start date
            initial_price = data.loc[data.index[0], 'Adj Close']
            final_price = data.loc[data.index[-1], 'Adj Close']
            initial_investment = 1000
            number_of_stocks = initial_investment / initial_price
            final_value = number_of_stocks * final_price
             
            

    # Format the explanation with consistent font and color
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
    # st.write('Risk Adj Return is', risk_adj_return_rounded, '%')

    # Optionally show detailed data
    show_data_checkbox = st.button('Show Detailed Data')
    if show_data_checkbox:
        st.write(data2)
        
elif sidebar_option == 'Track Portfolio':
     track_portfolio(ticker_options, default_ticker, default_start_date, default_end_date) 



        
    