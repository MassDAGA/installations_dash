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
```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Please Login')

password = st.text_input('Enter Password', type='password')

if st.button('Submit'):
   if password == 'PASSWORD':
       st.session_state.authenticated = True
   else:
       st.error('Incorrect password.')

st.stop()

st.title('MCF Installater Network')

csv_data = st.secrets['data']['csv']
installers = pd.read_csv(io.StringIO(csv_data))

st.dataframe(installers)

st.title('Installers Location Map')

fig_installers = px.scatter_mapbox(
   installers,
   lat='Latitude',
   lon='Longitude',
   hover_name='Installation Partner',
   hover_data=['Name'],
   zoom=5,
   color='Installation Partner',
   height=1000,
   width=2000,
)
fig_installers.update_layout(mapbox_style=“carto-darkmatter”, use_container_width=True)

st.plotly_chart(fig_installers)
 
