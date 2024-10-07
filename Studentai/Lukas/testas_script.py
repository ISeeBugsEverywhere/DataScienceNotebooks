import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt

from LKS94WGS84 import *


#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('Pasirinkti GMP failą ir gausim grafiką ')

f = st.file_uploader(label='CSV')
if f is not None:
    st.header('Nuskaitomas failas...')
    df = pd.read_csv(f)
    st.write('Nuskaita lentelė:')
    st.write(df.head(3))

    st.header('Skaičiuojami koordinačių stulpeliai "xai" ir "yai"')
    st.write('Papildyta lentelė:')
    df['xai'], df['yai'] = zip(*df.apply(lambda x: grid2geo(x['X'], x['Y']), 
                        axis=1))
    
    st.write(df.head(3))

    st.header('Sudaroma "mažų "gaisrų lentelė')

    mazi_gaisrai = df[df['zemesnis_ivykio_tipas'].str.contains('Gaisras 0|Gaisras 1|Gaisras 1AK' , na=False)]
# mazi_gaisrai.head(2)

    st.write(mazi_gaisrai.head(3))

    st.header('Braižomas grafikas')

    fig = px.scatter_mapbox(data_frame=mazi_gaisrai, lon='yai', lat='xai', zoom=5, title='Gaisrai iki 3 autocisternu')
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)

    st.header('Ačiū už dėmesį!')