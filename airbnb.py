import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Function to connect to MongoDB
def connect_to_mongo():
    try:
        # Access MongoDB connection URI from Streamlit secrets
        uri = st.secrets["mongo_uri"]["uri"]
        # Create a MongoClient instance
        client = MongoClient(uri)
        # Test the connection by pinging the server
        client.admin.command('ping')
        return client
    except ConnectionFailure as e:
        st.error(f"Could not connect to MongoDB: {e}")
        return None

# Main function to run the app
def main():
    st.title("Airbnb Data Analysis")

    # Attempt to connect to MongoDB
    client = connect_to_mongo()

    if client:
        # Replace with your database and collection names
        db = client["<your_database_name>"]  # Example: "airbnb_db"
        collection = db["<your_collection_name>"]  # Example: "listings"

        st.write("Connected to MongoDB!")

        # Fetch and display a sample document from the collection
        try:
            sample_data = collection.find_one()  # Fetch one document
            if sample_data:
                st.write("Sample Data from MongoDB:", sample_data)
            else:
                st.write("No data found in the collection.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Failed to connect to MongoDB.")

# Entry point for the app
if __name__ == "__main__":
    main()
