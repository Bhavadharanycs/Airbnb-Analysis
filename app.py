import streamlit as st
import pandas as pd
import plotly.express as px

def add_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZsXMOhp9z-A4-lOUBs4StVNKehZoiixPFbA&s');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to add the background image
add_bg_image()

# Load and clean data
@st.cache
def load_data():
    file_path = 'airbnb.csv' 
    df = pd.read_csv(file_path)
    
    # Convert price columns to numeric
    df['Price(in dollar)'] = pd.to_numeric(df['Price(in dollar)'], errors='coerce')
    df['Offer price(in dollar)'] = pd.to_numeric(df['Offer price(in dollar)'], errors='coerce')

    # Clean 'Review and rating' column by extracting rating
    df['Rating'] = df['Review and rating'].str.extract(r'(\d+\.\d+)').astype(float)
    
    # Extract number of beds as integer
    df['Number of bed'] = df['Number of bed'].str.extract(r'(\d+)').astype(float)
    
    return df

# Load data
df = load_data()

# Streamlit sidebar filters
st.sidebar.header("Filters")
price_range = st.sidebar.slider("Price Range", min_value=int(df['Price(in dollar)'].min()), max_value=int(df['Price(in dollar)'].max()), value=(50, 500))
rating = st.sidebar.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)

# Filter data based on selections
filtered_data = df[(df['Price(in dollar)'] >= price_range[0]) & (df['Price(in dollar)'] <= price_range[1]) & (df['Rating'] >= rating)]

# Main app
st.title("Airbnb Data Analysis")
st.write("Explore Airbnb listings with prices, ratings, and details.")

# Display data summary
st.write("### Data Summary")
st.write(filtered_data.describe())

# Price Distribution
st.write("### Price Distribution")
fig_price = px.histogram(filtered_data, x="Price(in dollar)", nbins=30, title="Price Distribution")
st.plotly_chart(fig_price)

# Ratings Analysis
st.write("### Ratings by Property")
fig_rating = px.histogram(filtered_data, x="Rating", nbins=20, title="Ratings Distribution")
st.plotly_chart(fig_rating)

# Show table of filtered results
st.write("### Filtered Listings")
st.dataframe(filtered_data[['Title', 'Price(in dollar)', 'Offer price(in dollar)', 'Rating', 'Number of bed']])

# Add an option to download the filtered data as a CSV for Power BI or Tableau
@st.cache
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_data)

st.download_button(
    label="Download filtered data as CSV for Power BI / Tableau",
    data=csv_data,
    file_name='filtered_airbnb_data.csv',
    mime='text/csv',
)
