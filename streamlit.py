import streamlit as st
import plotly.express as px
import pandas as pd
import datetime as dt
from PIL import Image

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.info()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def process_data(df):
    try:
        # Unpack lat and long from geodata
        df['lat'] = df['GeoData'].apply(lambda x: x.split(',')[0].replace('(', '').strip())
        df['long'] = df['GeoData'].apply(lambda x: x.split(',')[1].replace(')', '').strip())
        # Convert lat and long to float
        df['lat'] = df['lat'].astype(float)
        df['long'] = df['long'].astype(float)
        return df
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None

def plot_map(df):
    fig = px.scatter_mapbox(
        df, lat='lat', lon='long', hover_name='Account Name',
        hover_data=['Total Invoice Cost', 'Date Invoice Approved', 'Total Miles', 'Installing City', 'Service Order'],
        zoom=5, color='Installer Company', height=1000, size='Sum of Devices', width=1000
    )
    fig.update_layout(mapbox_style='carto-darkmatter')
    st.plotly_chart(fig)

def plot_bar_chart(df, title, x, y):
    st.title(title)
    bar_chart = px.bar(df, x=x, y=y, color='Installer Company', height=500)
    st.plotly_chart(bar_chart)

def main():
    # Configuration
    st.set_page_config(layout="wide")
    
    # Load data
    data_file_path = 'invoices_with_geodata.csv'
    df = load_data(data_file_path)
    if df is None:
        return
    
    # Process data
    df = process_data(df)
    if df is None:
        return
    
    # Load and display image
    image_path = 'Michelin_C_S_BlueBG_RGB_0621-01.png'
    try:
        image = Image.open(image_path)
        st.image(image, width=700)
        st.sidebar.image(image)
    except Exception as e:
        st.error(f"Error loading image: {e}")

    # Title
    st.title("Installations Map by Installer Company | 2023 to Current")
    st.sidebar.title("Filters")

    # Filters
    selected_installers = st.sidebar.multiselect("Select Installer Company", df['Installer Company'].unique())
    filtered_df = df[df['Installer Company'].isin(selected_installers)] if selected_installers else df

    selected_state = st.sidebar.multiselect("Select Installing State", df['Installing State'].unique())
    filtered_df = filtered_df[filtered_df['Installing State'].isin(selected_state)] if selected_state else filtered_df

    # Plot Map
    plot_map(filtered_df)

    # Plot Bar Charts
    plot_bar_chart(filtered_df, "Number of Installations by Installer Company", 'Installer Company', 'Sum of Devices')
    plot_bar_chart(filtered_df, "Total Invoice Cost by Installer Company", 'Date Invoice Approved', 'Total Invoice Cost')

    # Group Data and Plot Average Miles
    state_grouped = df.groupby(['Installing State', 'Installer Company'])['Total Miles'].mean().reset_index()
    plot_bar_chart(state_grouped, "Average Miles Traveled by Installer Company and State", 'Installing State', 'Total Miles')
    
    st.title("Average Miles Traveled by State")
    state_chart = px.bar(state_grouped, x='Installing State', y='Total Miles', color='Installer Company', height=500)
    state_chart.add_hline(y=state_grouped['Total Miles'].mean(), line_dash='dot', annotation_text='Average Miles Traveled')
    st.plotly_chart(state_chart)

if __name__ == "__main__":
    main()
