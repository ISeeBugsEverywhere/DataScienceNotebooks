import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='wide')

import requests

url = 'https://api.meteo.lt/v1/stations'
pg = requests.get(url)
r = pg.json()
stotys = {}
for i in r:
    stotys[i['name']] = i['code']
# print(stotys)
n = list(stotys.keys())

options = st.multiselect(
    "Select up to 3 stations:",
    options=n,
    max_selections=3,
)

st.write("You selected:", options)