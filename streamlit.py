import streamlit as st
import plotly.express as px
import pandas as pd
import io

def authenticate_user():
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

def load_data():
    csv_data = st.secrets["data"]["csv"]
    return pd.read_csv(io.StringIO(csv_data))

def create_map(data):
    fig = px.scatter_mapbox(
        data, lat='Latitude', lon='Longitude', hover_name='Installation Partner',
        hover_data=['Name'], zoom=5, color='Installation Partner', height=800
    )
    fig.update_layout(mapbox_style='carto-darkmatter', use_container_width=True)
    return fig

# Main application flow
authenticate_user()
st.title("MCF Installer Network")

installers = load_data()
st.dataframe(installers)

st.sidebar.title("Filters")
st.sidebar.header("Filters")  # Optional, can remove if redundant

st.title("Installers Location Map")
st.plotly_chart(create_map(installers))









