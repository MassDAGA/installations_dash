import streamlit as st
import plotly.express as px
import pandas as pd
import datetime as dt
from PIL import Image
import io




PASSWORD = st.secrets["password"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Login")
    password = st.text_input("Enter Password", type="password")
    if st.button("Submit"):
        if password == PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("Incorrect password.")
    st.stop()

st.title("MCF Installater Network")


# load CSV string
csv_data = st.secrets["data"]["csv"]
# read CSV from string
#df = pd.read_csv('/Users/massaerdiouf/Downloads/invoices_with_geodata.csv')
installers = pd.read_csv(io.StringIO(csv_data))

st.dataframe(installers)

# Title
st.title("Installers Location Map")
st.sidebar.title("Filters")



# Sidebar filters
st.sidebar.header("Filters")

# create interactive map with plotly from df_12_volts
fig_installers = px.scatter_mapbox(
    installers, lat='Latitude', lon='Longitude', hover_name='Installation Partner',
    hover_data=['Name'],
    zoom=5, color='Installation Partner', height=1000, width=1000
)
fig_installers.update_layout(mapbox_style='carto-darkmatter')
# Display the map
st.plotly_chart(fig_installers)












