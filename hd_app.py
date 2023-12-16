import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64

# Use the full page width
st.set_page_config(layout="wide")
# Function to set the background with transparency


def set_bg_hack(main_bg, main_bg_ext='png'):
    # CSS to inject contained in a string
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/{main_bg_ext};base64,{main_bg}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        opacity: 0.8; /* Adjust the transparency level here */
    }}

    /* Slightly opaque background for Streamlit elements for readability */
    .css-1d391kg, .css-1e5imcs, .css-1aumxhk, .css-hxt7ib, .css-18e3th9, .st-bx, .st-bw, .st-bv, .stButton > button {{
        background-color: rgba(255, 255, 255, 0.8) !important;
    }}

    /* Transparent background for Plotly charts */
    .js-plotly-plot .plotly, .plot-container .plotly {{
        background-color: transparent !important;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)


# Load the background image


@st.cache_data()
def get_image(image_file):
    with open(image_file, "rb") as file:
        img = file.read()
    return base64.b64encode(img).decode()


main_bg = get_image("background2.png")

# Set the background with transparency
set_bg_hack(main_bg)

# Load the dataset


@st.cache_data
def load_data():
    data = pd.read_csv('completed_flat_price_2017_2023.csv')
    return data


df = load_data()

# UI Enhancements
st.markdown('<style>h1{color: navy;}</style>', unsafe_allow_html=True)

# Sidebar for Filters
st.sidebar.header("Filters")
selected_town = st.sidebar.selectbox(
    "Select Town", options=df['town'].unique())

# Multiple selection dropdowns for flat_type and storey_range
selected_flat_types = st.sidebar.multiselect(
    "Select Flat Type(s)", options=df['flat_type'].unique(), default=df['flat_type'].unique())
selected_block = st.sidebar.selectbox(
    "Select Block", options=df[df['town'] == selected_town]['block'].unique())

available_storey_ranges = df['storey_range'].unique()
selected_storey_ranges = st.sidebar.multiselect(
    "Select Storey Range(s)", options=available_storey_ranges, default=available_storey_ranges)

# Filter Data based on selections
filtered_data = df[(df['town'] == selected_town) &
                   (df['flat_type'].isin(selected_flat_types)) &
                   (df['block'] == selected_block) &
                   (df['storey_range'].isin(selected_storey_ranges))]

# Update 'full_address' by removing 'Singapore'
filtered_data['full_address'] = filtered_data['full_address'].str.replace(
    " Singapore", "")

# Dynamic Chart Title
if not filtered_data.empty:
    chart_title = f"Resale Price Trend of {filtered_data['full_address'].iloc[0]} for {selected_flat_type}"
else:
    chart_title = "Resale Price Trend"

# Plotting
st.header("HDB Resale Price Trends", anchor=None)
fig = px.line(filtered_data, x='month', y='resale_price', title='')
fig.update_layout(
    title={
        'text': chart_title,
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24, 'color': 'black'}
    },
    xaxis_title="<b>Month</b>",
    yaxis_title="<b>Resale Price</b>",
    font=dict(family="Arial, sans-serif", size=18, color="black"),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        titlefont=dict(size=18, color='black'),
        tickfont=dict(size=16, color='black'),
        color='black'
    ),
    yaxis=dict(
        titlefont=dict(size=18, color='black'),
        tickfont=dict(size=16, color='black'),
        color='black'
    )
)
st.plotly_chart(fig, use_container_width=True)

# Data Table Adjustments
filtered_data = filtered_data[['full_address', 'month', 'town', 'flat_type', 'block', 'street_name',
                               'storey_range', 'floor_area_sqm', 'flat_model', 'lease_commence_date', 'remaining_lease', 'resale_price']]
st.header("Data Table")
st.dataframe(filtered_data, use_container_width=True)
