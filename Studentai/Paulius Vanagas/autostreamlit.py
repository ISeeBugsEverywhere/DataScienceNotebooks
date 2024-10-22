import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import plotly.express as px
import requests
from datetime import datetime, timedelta
import os

import streamlit as st
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='wide')

# @st.cache
#### pirmas blokas
SDB = sqlite3.connect('autoplius4.db') # jei neegsiztuoja - bus sukurfta nauja sqlite DB
Cs = SDB.cursor()

sql="""SELECT * FROM T1;"""
Cs.execute(sql)
ans = Cs.fetchall()
gamintojas, modelis, kaina, metai, kebulas, kuras, pavaros, galingumas, rida, nuorodos, pirmaregistracija, technikine = list(map(list, zip(*ans)))

df = pd.read_sql_query(sql, con=SDB)

# antras blokas

df['amzius']=2024-df['metai']

df['ridosintervalai'] = np.ceil(df['rida'] / 20000) * 20000

dfA=df[df['pavaros']=='Automatinė']
dfM=df[df['pavaros']=='Mechaninė']
dfgA = dfA[['amzius', 'kaina']].groupby('amzius').mean(numeric_only=True).reset_index()
dfgM = dfM[['amzius', 'kaina']].groupby('amzius').mean(numeric_only=True).reset_index()

fig1, axis1 = plt.subplots(figsize=[16, 6])
x = dfgA['amzius']
x2=dfgM['amzius']
w = 0.4
i = axis1.bar(x-w/2,dfgA['kaina'], label='Automatai', width=w)
o = axis1.bar(x2+w/2, dfgM['kaina'], label='Mechaninės', width=w)

axis1.set_xticks(x)
axis1.set_xticklabels(dfgA['amzius'])
axis1.set_xlim(left=min(x) - 1, right=20)
axis1.legend(loc='best')
axis1.set_xlabel('automobilio amžius')
axis1.set_ylabel('vidutinė auto kaina')
plt.title('autmomatinių ir mechaninių dėžių kainų palyginimas')
st.pyplot(fig1)

# trečias blokas

dfrida = df.groupby('ridosintervalai')['kaina'].mean().reset_index()

# Optionally, rename the columns for clarity
dfrida.columns = ['ridosintervalai', 'vidutinekaina']
dfrida['vidutinekaina']=round(dfrida['vidutinekaina'], 0)

fig2, axis2 = plt.subplots(figsize=(18, 6))

axis2.bar(dfrida['ridosintervalai'], dfrida['vidutinekaina'], width=18000)
axis2.set_xticks(dfrida['ridosintervalai'])
axis2.set_xticklabels(dfrida['ridosintervalai'], rotation=45)

axis2.set_xlabel('Ridos intervalai')
axis2.set_ylabel('vidutinė kaina')
plt.title('Vidutinė kaina nuo nuvažiuoto atstumo')

plt.tight_layout()
plt.show()

st.pyplot(fig2)

numbers = [fig1, fig2]

selected_number = st.selectbox('Select a number:', numbers)
st.write(f'Selected number: {selected_number}')

st.pyplot(selected_number)