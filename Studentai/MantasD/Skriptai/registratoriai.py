# https://data.gov.lt/datasets/2638/models/VietovesTemperaturaDregme/
# nuskaitykite šiuos duomenis (atsisiuntę kaip CSV ar kitu jums priimtinu būdu)
# atvaizduokite su scatter_mapbox, kuriose Lietuvos vietose yra įrengti registratoriai.
# atvaizduokite vieno bet kurio vietos registratoriaus užfiksuotas temperatūras (istorinius duomenis)
# 8 cm gylyje, paviršiuje, 15 cm aukštyje

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
import plotly.express as px

regs =  pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/VietovesTemperaturaDregme.csv')

fig = px.scatter_mapbox(data_frame=regs, lon='ilguma', lat='platuma', zoom=6.1)
fig.update_layout(mapbox_style='open-street-map')
fig.update_layout(width=800, height=600)
fig.show()