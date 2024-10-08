import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('Mano pirmasis Data Science puslapis')

f = st.file_uploader(label='CSV')
if f is not None:
    df = pd.read_csv(f)
    fig = px.scatter_mapbox(data_frame=df, lon='X', lat='Y', zoom=6.1)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(width=800, height=600)
    fig.show()