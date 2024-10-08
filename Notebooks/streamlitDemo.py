import streamlit as st
import pandas as pd
# import numpy as np
import plotly.express as px
# import mysql.connector as cnt
# import matplotlib.pyplot as plt
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='wide')
from LKS94WGS84 import grid2geo
df = None # df 

@st.cache_data
def load_csv(path):
    d = pd.read_csv(path)
    return d

@st.cache_data
def konvert(df):
    x = df.loc[:,'X'].values
    y = df.loc[:,'Y'].values
    lat, lon = zip(*list(map(grid2geo, x, y)))
    df['LAT'] = lat
    df['LONG'] = lon
    return df

file = st.file_uploader('CSV!')
if file is not None:
    df = load_csv(file)

if df is not None:
    df = konvert(df)
    st.write(df.head())
    
left, right = st.columns(2)
if df is not None:
    dfg = df[~df['zemesnis_ivykio_tipas'].str.contains('Gaisras 0', na=False)]
    fig = px.scatter_mapbox(data_frame=dfg, lon='LONG', lat='LAT', zoom=6)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(title='Gaisrų žemėlapis')
    fig.update_layout(width=800, height=600)
    left.plotly_chart(fig)
    #  KET
    dfg = df[df['zemesnis_ivykio_tipas'].str.contains('KET', na=False)]
    fig = px.scatter_mapbox(data_frame=dfg, lon='LONG', lat='LAT', zoom=6)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(title='KET pažeidimų vietos')
    fig.update_layout(width=800, height=600)
    right.plotly_chart(fig)