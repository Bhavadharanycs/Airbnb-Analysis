import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Airbnb dataset
@st.cache
def load_data():
    file_path = '/mnt/data/airbnb.csv'
    df = pd.read_csv(file_path)
    
    # Basic cleaning
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['latitude', 'longitude', 'price'], inplace=True)  # Drop rows missing essential data
    df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert price to numeric
    df['price'] = df['price'].fillna(df['price'].median())  # Fill missing prices with median
    df['availability_365'] = pd.to_numeric(df['availability_365'], errors='coerce')  # Ensure availability is numeric
    return df

# Load and display data
df = load_data()

# Streamlit sidebar filters
st.sidebar.header("Filters")
location = st.sidebar.multiselect("Select Neighborhood", options=df['neighborhood'].unique())
property_type = st.sidebar.multiselect("Select Property Type", options=df['property_type'].unique())
price_range = st.sidebar.slider("Price Range", min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(50, 300))

# Filter data based on sidebar inputs
filtered_data = df.copy()
if location:
    filtered_data = filtered_data[filtered_data['neighborhood'].isin(location)]
if property_type:
    filtered_data = filtered_data[filtered_data['property_type'].isin(property_type)]
filtered_data = filtered_data[(filtered_data['price'] >= price_range[0]) & (filtered_data['price'] <= price_range[1])]

# Main app title and description
st.title("Airbnb Data Analysis")
st.write("Explore Airbnb listings, analyze prices, and check availability patterns.")

# Show basic data summary
st.write("### Data Summary")
st.write(filtered_data.describe())

# Map Visualization
st.write("### Map of Airbnb Listings")
fig = px.scatter_mapbox(
    filtered_data,
    lat='latitude',
    lon='longitude',
    color='price',
    size='availability_365',
    color_continuous_scale='Viridis',
    size_max=10,
    zoom=10,
    mapbox_style="carto-positron",
    hover_name='neighborhood',
    hover_data={'price': True, 'property_type': True, 'availability_365': True}
)
st.plotly_chart(fig)

# Price Analysis
st.write("### Price Distribution by Neighborhood")
fig_price = px.box(filtered_data, x="neighborhood", y="price", color="neighborhood")
st.plotly_chart(fig_price)

# Availability Patterns
st.write("### Availability Distribution")
fig_availability = px.histogram(filtered_data, x="availability_365", nbins=30)
st.plotly_chart(fig_availability)
