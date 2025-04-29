import streamlit as st
import plotly.express as px
import pandas as pd
import datetime as dt
from PIL import Image




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

st.title("Welcome to the App 🎉")


# load CSV string
csv_data = st.secrets["data"]["csv"]
read CSV from string
#df = pd.read_csv('/Users/massaerdiouf/Downloads/invoices_with_geodata.csv')
installers = pd.read_csv(io.StringIO(csv_data))



# unpack lat and long from geodata
#df['lat'] = df['GeoData'].apply(lambda x: x.split(',')[0])
#df['long'] = df['GeoData'].apply(lambda x: x.split(',')[1])

# remove opening and closing parentheses from lat and long
#df['lat'] = df['lat'].str.replace('(', '')
#df['long'] = df['long'].str.replace(')', '')

# convert lat and long to float
#df['lat'] = df['lat'].astype(float)
#df['long'] = df['long'].astype(float)



# Streamlit UI

# add a .png image to the page as a header

#image = Image.open('/Users/massaerdiouf/Desktop/Michelin_C_S_BlueBG_RGB_0621-01.png')
# insert an image to the page
#st.image(image, width=800)

# insert image to the sidebar
st.sidebar.image(image)


# Title
st.title("Installers Location Map")
st.sidebar.title("Filters")

# FILTERS

# Convert date column to datetime format
#df['Date Invoice Approved'] = pd.to_datetime(df['Date Invoice Approved'])


# Sidebar filters
st.sidebar.header("Filters")

# Date Range Filter
'''min_date = df['Date Invoice Approved'].min().date()
max_date = df['Date Invoice Approved'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Filter by Date Invoice Approved", 
    [min_date, max_date], 
    min_value=min_date, 
    max_value=max_date
)
'''

# Filter DataFrame by Date Range
'''filtered_df = df[(df['Date Invoice Approved'] >= pd.Timestamp(start_date)) & 
                 (df['Date Invoice Approved'] <= pd.Timestamp(end_date))]'''

# Filter by Installer Company
'''selected_installers = st.sidebar.multiselect("Select Installer Company", df['Installer Company'].unique())
filtered_df = filtered_df[filtered_df['Installer Company'].isin(selected_installers)] if selected_installers else filtered_df

# Filter by Installing State
selected_state = st.sidebar.multiselect("Select Installing State", df['Installing State'].unique())
filtered_df = filtered_df[filtered_df['Installing State'].isin(selected_state)] if selected_state else filtered_df

# Filter by Installing Country
selected_country = st.sidebar.multiselect("Select Installing Country", df['Installing Country'].unique())
filtered_df = filtered_df[filtered_df['Installing Country'].isin(selected_country)] if selected_country else filtered_df

# Display Results
st.write(f"Showing invoices approved between {start_date} and {end_date}:")
st.dataframe(filtered_df)
'''



# Plotly Map
'''fig = px.scatter_mapbox(
    filtered_df, lat='lat', lon='long', hover_name='Account Name',
    hover_data=['Total Invoice Cost', 'Date Invoice Approved', 'Total Miles', 'Installing City', 'Service Order'],
    zoom=5, color='Installer Company', height=1000, size='Sum of Devices', width=1000
)
fig.update_layout(mapbox_style='carto-darkmatter')
'''

# create interactive map with plotly from df_12_volts
fig_installers = px.scatter_mapbox(
    installers, lat='Latitude', lon='Longitude', hover_name='Installation Partner',
    hover_data=['Name'],
    zoom=5, color='Installation Partner', height=1000, width=1000
)
fig_installers.update_layout(mapbox_style='carto-darkmatter')
st.plotly_chart(fig)
# Display the map
st.plotly_chart(fig_installers)


# insert an interactive bart chart showing the number of installations by installer company
'''st.title("Number of Installations by Installer Company")
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
'''










