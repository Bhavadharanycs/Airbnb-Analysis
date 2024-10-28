import streamlit as st
import pandas as pd

# Function to load data from a CSV file
def load_data(file_path):
    try:
        # Load data into a DataFrame
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Main function to run the app
def main():
    st.title("Airbnb Data Analysis (Without MongoDB)")

    # Provide a path to your CSV file
    file_path = "airbnb.csv"  # Replace with your actual CSV file path

    # Load the data
    data = load_data(file_path)

    if data is not None:
        st.write("Data Loaded Successfully!")

        # Display the first few rows of the data
        st.write("Sample Data:")
        st.dataframe(data.head())

        # Add any data analysis or visualization logic here
        st.write("Summary Statistics:")
        st.write(data.describe())

        # Further charts/visualizations can be added here
        st.line_chart(data['price'])  # Example: Line chart of Airbnb prices
    else:
        st.error("Failed to load data.")

# Entry point for the app
if __name__ == "__main__":
    main()
