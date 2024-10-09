# Leiskite vartotojui nurodyti iki trijų metreologinių stočių, ir dvi datas : nuo, iki.
# Iš mateo.lt per API išgaukite istorinius duomenis nurodytame laikotarpyje, 
# ir atvaizduokite grafiškai - oro temperatūrą bei vėjo greitį.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
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

today = datetime.date.today()- datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)
start_date = st.date_input('Data nuo', today)
end_date = st.date_input('Data iki', tomorrow)
if start_date < end_date:
    st.success('Data nuo: `%s`\n\nData iki: `%s`' % (start_date, end_date))
else:
    st.error('Klaida: Pabaigos ir pradžios datos vienodos')
    
dates = np.arange(start_date, end_date+datetime.timedelta(days=1), datetime.timedelta(days=1)).tolist()
ndates = []
for date in dates:
    date = str(date)[:10]
    ndates.append(date)
st.write("You selected:", ndates)

avg_temps = []
stations = []
dates_stations = []

for station in options:
    s = stotys[station]
    for date in ndates:
        url = f'https://api.meteo.lt/v1/stations/{s}/observations/{date}'
        request = requests.get(url)
        observations = request.json()['observations']
        temps = []
        for obs in observations:
            temps.append(obs['airTemperature'])
        avg_temp = sum(temps)/len(temps)
        avg_temps.append(avg_temp)
        stations.append(station)
        dates_stations.append(date)
    

df = pd.DataFrame(avg_temps)
df['Temperatūra'] = pd.DataFrame(data=avg_temps)
df['Stotis'] = pd.DataFrame(data=stations)
df['Date'] = pd.DataFrame(data=dates_stations)
df['Date'] = pd.to_datetime(df['Date'])

fig, axes = plt.subplots(figsize=(10,6))

axes.set_title('Temperatūros')
ax = sns.lineplot(data=df,x = 'Date', y='Temperatūra', ax=axes, hue='Stotis')
axes.set(xlabel='Data ir laikas',ylabel='Temperatūra')
st.pyplot(fig)


# https://data.gov.lt/datasets/2638/models/VietovesTemperaturaDregme/
# nuskaitykite šiuos duomenis (atsisiuntę kaip CSV ar kitu jums priimtinu būdu)
# atvaizduokite su scatter_mapbox, kuriose Lietuvos vietose yra įrengti registratoriai.
# atvaizduokite vieno bet kurio vietos registratoriaus užfiksuotas temperatūras (istorinius duomenis)
# 8 cm gylyje, paviršiuje, 15 cm aukštyje

# regs =  pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/VietovesTemperaturaDregme.csv')

# fig = px.scatter_mapbox(data_frame=regs, lon='ilguma', lat='platuma', zoom=6.1)
# fig.update_layout(mapbox_style='open-street-map')
# fig.update_layout(width=800, height=600)
# st.pyplot(fig)