import streamlit as st
import plotly.express as px
import pandas as pd
import datetime as dt

# load data
df = pd.read_csv('/Users/massaerdiouf/Downloads/invoices_with_geodata.csv')
df.info()

# unpack lat and long from geodata
df['lat'] = df['GeoData'].apply(lambda x: x.split(',')[0])
df['long'] = df['GeoData'].apply(lambda x: x.split(',')[1])

# remove opening and closing parentheses from lat and long
df['lat'] = df['lat'].str.replace('(', '')
df['long'] = df['long'].str.replace(')', '')

# convert lat and long to float
df['lat'] = df['lat'].astype(float)
df['long'] = df['long'].astype(float)

# Set the page layout to wide
st.set_page_config(layout="wide")


# Streamlit UI

# add a .png image to the page as a header
from PIL import Image
image = Image.open('/Users/massaerdiouf/Desktop/Michelin_C_S_BlueBG_RGB_0621-01.png')
# insert an image to the page
st.image(image, width=700)

# insert image to the sidebar
st.sidebar.image(image)


# Title
st.title("Installations Map by Installer Company | 2023 to Current")
st.sidebar.title("Filters")

# FILTERS

# Filter DataFrame based on selection
selected_installers = st.sidebar.multiselect("Select Installer Company", df['Installer Company'].unique())
filtered_df = df[df['Installer Company'].isin(selected_installers)] if selected_installers else df

# create a filter for the Installating State on the sidebar
selected_state = st.sidebar.multiselect("Select Installing State", df['Installing State'].unique())
filtered_df = filtered_df[filtered_df['Installing State'].isin(selected_state)] if selected_state else filtered_df

# Plotly Map
fig = px.scatter_mapbox(
    filtered_df, lat='lat', lon='long', hover_name='Account Name',
    hover_data=['Total Invoice Cost', 'Date Invoice Approved', 'Total Miles', 'Installing City', 'Service Order'],
    zoom=5, color='Installer Company', height=1000, size='Sum of Devices', width=1000
)
fig.update_layout(mapbox_style='carto-darkmatter')

# Show map
st.plotly_chart(fig)

# insert an interactive bart chart showing the number of installations by installer company
st.title("Number of Installations by Installer Company")
bar_chart = px.bar(filtered_df, x='Installer Company', y='Sum of Devices', color='Installer Company', height=500)
st.plotly_chart(bar_chart)

# insert an interactive line chart showing the total invoice cost by installer company
st.title("Total Invoice Cost by Installer Company")
line_chart = px.bar(filtered_df, x='Date Invoice Approved', y='Total Invoice Cost', color='Installer Company', height=500)
st.plotly_chart(line_chart)

# group the data frame by Installing State and Installer Company and calculate the average miles traveled
state_grouped = df.groupby(['Installing State', 'Installer Company'])['Total Miles'].mean().reset_index()

# visualize the average miles traveled by installer company and state
st.title("Average Miles Traveled by Installer Company and State")
state_chart = px.bar(state_grouped, x='Installing State', y='Total Miles', color='Installer Company', height=500)
st.plotly_chart(state_chart)

# average miles travelled by state in descending order with a reference line for the average miles traveled and a filter for the installer company
st.title("Average Miles Traveled by State")
state_chart = px.bar(state_grouped, x='Installing State', y='Total Miles', color='Installer Company', height=500)
state_chart.add_hline(y=state_grouped['Total Miles'].mean(), line_dash='dot', annotation_text='Average Miles Traveled')
st.plotly_chart(state_chart)











