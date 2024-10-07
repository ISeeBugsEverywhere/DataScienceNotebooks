import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Setting up the Streamlit page configuration
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('My First Data Science Web Page')

# Function to read JSON files
def read_json(file):
    df = pd.read_json(file)
    return df

# Cached version of the read_json function to avoid reloading the data upon each interaction
@st.cache
def read_json_cached(file):
    df = pd.read_json(file)
    return df

# Creating two columns for different file uploads
left, right = st.columns(2)

# File uploader on the left
file_left = left.file_uploader(label='Select a JSON file (left)')

left.write('Simple Function')
if file_left is not None:
    df_left = read_json(file_left)
    left.write(df_left.head(5))

# File uploader on the right
file_right = right.file_uploader(label='Select a JSON file (right)')

right.write('Cached Function')
if file_right is not None:
    df_right = read_json_cached(file_right)
    right.write(df_right.head(5))



f = st.file_uploader(label='CSV')
if f is not None:
df = pd.read_csv(f)
fig = px.scatter_mapbox(data_frame=df, lon='X', lat='Y', zoom=5)
fig.update_layout(mapbox_style='open-street-map')
fig.update_layout(width=800, height=600)
st.plotly_chart(fig)




