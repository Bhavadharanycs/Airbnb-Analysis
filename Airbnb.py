import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import geopandas as gpd
from streamlit_folium import folium_static
import folium
import streamlit as st
from pymongo import MongoClient

def connect_to_mongo():
    # Check available secrets
    st.write(st.secrets)
    
    # Access MongoDB connection URI
    uri = st.secrets["mongo_uri"]["uri"]
    client = MongoClient(uri)
    return client["dbname"]["collection_name"]  # Replace with actual database and collection

# Use the connection in your app
collection = connect_to_mongo()
st.write("Connected to MongoDB!")


# MongoDB connection
def connect_to_mongo(uri, db_name, collection_name):
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection

# Fetch data from MongoDB
def fetch_data(collection):
    data = list(collection.find())
    df = pd.DataFrame(data)
    return df

# Data Cleaning and Preparation
def clean_data(df):
    # Example: Handling missing values, type conversion
    df = df.drop_duplicates()
    df['price'] = df['price'].replace({'$': '', ',': ''}, regex=True).astype(float)
    df.dropna(subset=['latitude', 'longitude'], inplace=True)  # Drop rows with missing geo-coordinates
    return df

# Geospatial Visualization: Interactive Map
def plot_map(df):
    # Create a Folium map centered around average latitude and longitude
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Add markers to the map
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Price: {row['price']}, Rating: {row['rating']}"
        ).add_to(m)

    folium_static(m)

# Dynamic Plot: Price Analysis
def plot_price_analysis(df):
    fig = px.scatter(df, x='longitude', y='latitude', color='price', 
                     hover_data=['name', 'price', 'room_type'],
                     title="Airbnb Listings: Price Analysis")
    st.plotly_chart(fig)

# Main Streamlit Application
def main():
    st.title("Airbnb Data Analysis")

    # MongoDB connection details
    uri = st.secrets["mongo_uri"]
    db_name = "airbnb_db"
    collection_name = "listings"

    # Fetch and clean data
    collection = connect_to_mongo(uri, db_name, collection_name)
    df = fetch_data(collection)
    df = clean_data(df)

    # Sidebar filters
    st.sidebar.title("Filters")
    room_type = st.sidebar.multiselect("Room Type", options=df['room_type'].unique(), default=df['room_type'].unique())
    df_filtered = df[df['room_type'].isin(room_type)]

    # Display interactive map
    st.header("Geospatial Distribution of Listings")
    plot_map(df_filtered)

    # Price Analysis
    st.header("Price Analysis")
    plot_price_analysis(df_filtered)

    # Further charts/visualizations can be added here (e.g., seasonal availability, location-based insights)
    
if __name__ == "__main__":
    main()

