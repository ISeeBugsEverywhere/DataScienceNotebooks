import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(page_icon=':bar_chart:', page_title='DEMO STREAMLIT MAP', layout='centered')

# Header
st.header('Mano pirmas data science web puslapis')

# Define a function to read a JSON file
def read_json(name):
    df = pd.read_json(name)
    return df

# Define a cached function to read a JSON file
@st.cache_data
def read_json_cached(name):
    dff = pd.read_json(name)
    return dff

# File uploader
file = st.file_uploader(label='Nurodykite JSON failą')

# Create two columns
left, right = st.columns(2)

left.write('Paprasta funkcija')
if file is not None:
    # Read the file using the non-cached function
    df = read_json(file)
    left.write(df.head(5))

right.write('Dekoruota funkcija')
if file is not None:
    # Read the file using the cached function
    dff = read_json_cached(file)
    right.write(dff.head(5))