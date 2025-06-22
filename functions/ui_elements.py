import streamlit as st
import time

# Function to create typing animation
def typing_animation(text, speed=0.05):
    animated_text = ''
    placeholder = st.empty()
    for char in text:
        animated_text += char
        placeholder.markdown(f'<p style="font-size:24px; color:#83B4FF; font-weight:bold;">{animated_text}</p>', unsafe_allow_html=True)
        time.sleep(speed)

@st.cache_data
def render_header_and_text():
    # Header
    st.title("Stock Analysis Dashboard")

    # Text with typing animation
    lines = [
        "Welcome!!!",
        "Select a stock from the sidebar to get started.",
    ]

    for line in lines:
        typing_animation(line)
        time.sleep(1)


def render_layout_with_image():
    # Create a layout with three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Place the image in the center column
    with col2:
        st.image('logos/test.svg', width=300)
        
        
# Call the function to render layout with image
def render_portfolio_layout_with_image():
    # Create a layout with three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Place the image in the center column
    with col2:
        st.image('logos/portfolio_image.svg', width=300)
    
@st.cache_data
# Call the cached function to render header and text
def render_portfolio_header_and_text():
    # Header
    st.title("Portfolio Analysis Dashboard")

    # Text with typing animation
    lines = [
        "Welcome!!!",
        "You can now track your portfolio here.",
    ]

    for line in lines:
        typing_animation(line)
        time.sleep(1)
