import streamlit as st
import plotly.express as px
import pandas as pd
import datetime as dt
from PIL import Image

# Configuration
st.set_page_config(layout="wide")


def main():
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            # Read the uploaded CSV file
            df = pd.read_csv(uploaded_file)
            st.write("Data Preview:", df.head())  # Display first few rows

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

        except Exception as e:
            st.error(f"Error reading the uploaded file: {e}")
    else:
        st.warning("Please upload a CSV file.")

# Streamlit file uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

def process_data(df):
    """
    Process the dataframe to extract latitude and longitude from GeoData.
    Args:
        df (pd.DataFrame): Input dataframe with GeoData column.

    Returns:
        pd.DataFrame: DataFrame with 'lat' and 'long' columns.
    """
    try:
        # Unpack lat and long from geodata
        df[['lat', 'long']] = df['GeoData'].str.extract(r'\(([^,]+), ([^,]+)\)')
        # Convert lat and long to float
        df['lat'] = df['lat'].astype(float)
        df['long'] = df['long'].astype(float)
        return df
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None

def plot_map(df):
    """
    Plot a scatter mapbox using the dataframe.
    Args:
        df (pd.DataFrame): DataFrame with latitude and longitude information.
    """
    fig = px.scatter_mapbox(
        df, lat='lat', lon='long', hover_name='Account Name',
        hover_data=['Total Invoice Cost', 'Date Invoice Approved', 'Total Miles', 'Installing City', 'Service Order'],
        zoom=5, color='Installer Company', height=1000, size='Sum of Devices', width=1000
    )
    fig.update_layout(mapbox_style='carto-darkmatter')
    st.plotly_chart(fig)

def plot_bar_chart(df, title, x, y):
    """
    Plot a bar chart using the dataframe.
    Args:
        df (pd.DataFrame): DataFrame for plotting.
        title (str): Title of the chart.
        x (str): Column name for x-axis.
        y (str): Column name for y-axis.
    """
    st.title(title)
    bar_chart = px.bar(df, x=x, y=y, color='Installer Company', height=500)
    st.plotly_chart(bar_chart)


if __name__ == "__main__":
    main()

