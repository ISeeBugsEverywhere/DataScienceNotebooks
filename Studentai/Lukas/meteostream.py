import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import requests
import seaborn as sns

from datetime import date, timedelta
from dateutil import parser
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='wide')



url = 'https://api.meteo.lt/v1/stations'
pg = requests.get(url)
r = pg.json()
stotys = {}
for i in r:
    stotys[i['name']] = i['code']
# print(stotys)
n = list(stotys.keys())
kodai = list(stotys.values())

options = st.multiselect(
    "Select up to 3 stations:",
    options=n,
    max_selections=3,
)

st.write("You selected:", options)


# stations = input('Įveskite stoties numerį(-ius) (iki trijų numerių, atskirtų kableliais)')
# st_idx = list(map(int, options.split()))
# print('Jūs pasirinkote šias stotis:')
# sel_sts = [n[i] for i in st_idx]
# sel_kodai = [kodai[i] for i in st_idx]
# print(sel_sts)
# print(sel_kodai)

nuo = st.text_input(label='nuo kada (yyyy-mm-dd)?')
iki = st.text_input(label='iki kada (yyyy-mm-dd)?')

datos = []
laikai = []

start_date = parser.parse(nuo)
end_date = parser.parse(iki)
delta = timedelta(days=1)
while start_date <= end_date:
    print(start_date.strftime("%Y-%m-%d"))
    datos.append(str(start_date))
    start_date = start_date + delta
    
    
for i in datos:
    laikai.append(i[:10])


stotys_new= []
data = []
temperatura = []
vejas = []

for station in options:
    s = stotys[station]
    for d in laikai:
        # s = stotys[station]
        url2 = f'https://api.meteo.lt/v1/stations/{s}/observations/{d}'
        observations = requests.get(url2).json()['observations']
        for o in observations:
            stotys_new.append(station)
            data.append(o['observationTimeUtc'])
            temperatura.append(o['airTemperature'])
            vejas.append(o['windSpeed'])




ndf = pd.DataFrame(data)
ndf['Kodas'] = pd.DataFrame(data=stotys_new)
ndf['Temperatūros'] = pd.DataFrame(data=temperatura)
ndf['Data'] = pd.DataFrame(data=data)
ndf['vejasSpeed'] = pd.DataFrame(data=vejas)

ndf['Datos'] = pd.to_datetime(ndf['Data'])
ndf['Laikai'] = pd.to_datetime(ndf['Data']).dt.time

fig, axes = plt.subplots(figsize=(8, 4.5))

axes.set_title('Temperatūros')
ax = sns.lineplot(data=ndf,x = 'Datos', y='Temperatūros', ax=axes, hue='Kodas', palette='Set2', style='Kodas')
axes.set(xlabel='Laikas',ylabel='Temperatura')
# axes.set_xticks(data)
axes.tick_params(axis='x', rotation=90, labelsize=6)
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig)


fig, axes = plt.subplots(figsize=(8, 4.5))

axes.set_title('Vėjas')
ax = sns.lineplot(data=ndf,x = 'Datos', y='vejasSpeed', ax=axes, hue='Kodas', palette='Set2', style='Kodas')
axes.set(xlabel='Laikas',ylabel='Vėjo greitis m/s')
# axes.set_xticks(data)
axes.tick_params(axis='x', rotation=90, labelsize=6)
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig)