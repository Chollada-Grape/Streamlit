import streamlit as st
import numpy as np
import pandas as pd

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

#data
st.subheader('Raw data')
st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hist_values_test = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))
st.bar_chart(hist_values_test)

st.subheader('Map of all pickups')
st.map(data)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# Exercise 1: Convert 2D map to 3D map using PyDeck
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.header("3D Map using PyDeck")

chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"]
)

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=chart_data,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
                pickable=True,
            )
        ],
    )
)

# Exercise 2: Use Date input
import streamlit as st
from datetime import date

st.header("Date Input Example")

selected_date = st.date_input("Select a date")
st.write("You selected:", selected_date)

# Exercise 3: Use Selectbox
st.header("Selectbox - Filter pickups by hour")

# Create Selectbox to choose hour
unique_hours = sorted(data[DATE_COLUMN].dt.hour.unique())
selected_hour = st.selectbox("Select an hour", unique_hours)

# Filter data based on selected hour
filtered_data_selectbox = data[data[DATE_COLUMN].dt.hour == selected_hour]

# Display filtered data on map
st.subheader(f"Map of pickups at {selected_hour}:00")
st.map(filtered_data_selectbox)

# Exercise 4: Use Plotly (any chart)
import plotly.express as px

st.header("Plotly Chart - Pickups by Hour")

# Calculate histogram values for hours
hour_counts = data[DATE_COLUMN].dt.hour.value_counts().sort_index()
hour_df = pd.DataFrame({'hour': hour_counts.index, 'pickups': hour_counts.values})

# Plot using Plotly
fig = px.bar(hour_df, x='hour', y='pickups', title='Number of Uber pickups by hour')
st.plotly_chart(fig)

# Exercise 5: Click a button to increase the number X

if "count_button" not in st.session_state:
    st.session_state.count_button = 0
 
if st.button("Run it again"):
    st.session_state.count_button += 1
 
if st.button("Reset", type="primary"):
    st.session_state.count_button = 0
 
st.header(f"Count_button clicked: {st.session_state.count_button}")