import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import geopandas as gpd
from streamlit_folium import folium_static
import folium

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

   
