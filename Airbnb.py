import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings


warnings.filterwarnings('ignore')
st.set_page_config(page_title="AIRBNB-Analysis",layout="wide")
def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background:url("Home.jpg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)


setting_bg()

# Creating options menu
select = option_menu(
    menu_title=None,
    options=["About", "Explore", "Creator"],
    icons=["house", "search", "person-circle"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#004791"},
            "nav-link-selected": {"background-color": "#004791"}})

# configuring about
if select=="About":
    st.markdown("### :blue[Domain]: Travel Industry, Property Management and Tourism ")
    st.markdown("### :blue[Technologies used]: Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb, PowerBI or Tableau")
    st.markdown("### :blue[Overall]: This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends")

# configuring explore
if select == "Explore":
 fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
 if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
 else:
    df = pd.read_csv("Airbnb_data.csv", encoding="ISO-8859-1")
 #creating sidebar
 st.sidebar.header("Choose Filter: ")
  
 neighbourhood_group = st.sidebar.multiselect("Pick Neighbourhood_group", df["Neighbourhood_group"].unique())
 if not neighbourhood_group:
     df2 = df.copy()
 else:
     df2 = df[df["Neighbourhood_group"].isin(neighbourhood_group)]

 neighbourhood = st.sidebar.multiselect("Pick the Neighbourhood", df2["Neighbourhood"].unique())
 if not neighbourhood:
     df3 = df2.copy()
 else:
     df3 = df2[df2["Neighbourhood"].isin(neighbourhood)]

 if not neighbourhood_group and not neighbourhood:
     filtered_df = df
 elif not neighbourhood:
     filtered_df = df[df["Neighbourhood_group"].isin(neighbourhood_group)]
 elif not neighbourhood_group:
     filtered_df = df[df["Neighbourhood"].isin(neighbourhood)]
 elif neighbourhood:
     filtered_df = df3[df["Neighbourhood"].isin(neighbourhood)]
 elif neighbourhood_group:
     filtered_df = df3[df["Neighbourhood_group"].isin(neighbourhood_group)]
 elif neighbourhood_group and neighbourhood:
     filtered_df = df3[df["Neighbourhood_group"].isin(neighbourhood_group) & df3["Neighbourhood"].isin(neighbourhood)]
 else:
     filtered_df = df3[df3["Neighbourhood_group"].isin(neighbourhood_group) & df3["Neighbourhood"].isin(neighbourhood)]
 
 room_type_df = filtered_df.groupby(by=["Room_type"], as_index=False)["Price"].sum()

 col1, col2 = st.columns(2)
 with col1:
    st.subheader("Type of Rooms")
    fig = px.bar(room_type_df, x="Room_type", y="Price", text=['${:,.2f}'.format(x) for x in room_type_df["Price"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

 cl1, cl2 = st.columns((2))
 with cl1:
    with st.expander("Room wise price table"):
        st.write(room_type_df.style.background_gradient(cmap="Blues"))
        csv = room_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Room_type.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')
 
 with cl2:
    with st.expander("Neighbourhood group wise price"):
        neighbourhood_group = filtered_df.groupby(by="Neighbourhood_group", as_index=False)["Price"].sum()
        st.write(neighbourhood_group.style.background_gradient(cmap="Blues"))
        csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Neighbourhood_group.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')
  #creating scatterplot      
 data1 = px.scatter(filtered_df, x="Neighbourhood_group", y="Neighbourhood", color="Room_type")
 data1['layout'].update(title="Rooms in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
 st.plotly_chart(data1, use_container_width=True)

 with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
     st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Blues"))
 csv = df.to_csv(index=False).encode('utf-8')
 st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

 import plotly.figure_factory as ff

 st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
 with st.expander("Summary_Table"):
    df_sample = df[0:5][["Neighbourhood_group", "Neighbourhood",  "Room_type", "Price", "Minimum_nights", "Host_name"]]
    fig = ff.create_table(df_sample, colorscale="Blues")
    st.plotly_chart(fig, use_container_width=True)
 

if select=="Creator":
    st.write('------------------')
    col3,col4=st.columns(2)
    image=Image.open('airbnb.png')
    with col3:
     col3.markdown("### :blue[NAME] : ***M GOBINATH***")
     col3.markdown("### :blue[Mail ID] : ***gobimurugan71@gmail.com***")
     col3.markdown("### :blue[GITHUB URL] : ***https://github.com/Go7bi***")
     col3.markdown('### :blue[ ***Data Scientist Aspirant***]')
    with col4:
        st.image(image) 
