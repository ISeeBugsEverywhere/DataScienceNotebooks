import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import sqlite3

#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('Kainos priklausomybė nuo ridos ')

SDB = sqlite3.connect('Auto2.db')
Cs = SDB.cursor()

sql="""select * from Autopliuslt;"""
df_with_dubs = pd.read_sql_query(sql, con=SDB)
df = df_with_dubs.drop_duplicates()

def rida(x):
    if x != 'None':
        return int(x.replace(' ', '').replace('km', ''))
    else:
        return 'None'
        

def kaina(x):
    if x != 'None':
        return int(x.replace(' ', ''))

def amzius(x):
    if x != 'None':
        return int(2024 - int(x[:4]))

def galia(x):
    if 'kW' in x:
        return int(x.split('(')[-1][:-3])
    else:
        return 'None'
    
df['price'] = df['Kaina'].apply(kaina)
df['amzius'] = df['PirmaRegistracija'].apply(amzius)
df['rid'] = df['Rida'].apply(rida)
df['galia'] = df['Variklis'].apply(galia)
# df.head()
df['R5000'] = df[df['rid'] != 'None']['rid'].apply(lambda x: int(np.ceil(x/5000) * 5000))

df_rid_gr = df[['R5000', 'price']].groupby('R5000').mean(numeric_only=True).reset_index()

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.scatterplot(data=df_rid_gr, x=df_rid_gr['R5000'], y=df_rid_gr['price'], label='vid. kaina')
ax.set_xlabel('Rida sugrupuotas kas 5000 km')
ax.set_ylabel('Kainos vidurkis')
st.pyplot(fig, use_container_width=True)


st.header('Kainos priklausomybė nuo automobilio amžiaus ')
df_amz_gr = df[['amzius', 'price']].groupby('amzius').mean(numeric_only=True).reset_index()
fig, ax = plt.subplots(figsize=(12, 4.5))

sns.barplot(data=df_amz_gr, x=df_amz_gr['amzius'], y=df_amz_gr['price'], palette='Set2')
ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)
st.pyplot(fig, use_container_width=True)



st.header('Kainos priklausomybė nuo automobilio galios ')
df['galia50'] = df[df['galia'] != 'None']['galia'].apply(lambda x: (np.ceil(x/25) * 25))
df_galia_gr = df[['galia50', 'price']].groupby('galia50').mean(numeric_only=True).reset_index()


fig, ax = plt.subplots(figsize=(12, 4.5))

sns.lineplot(data=df_galia_gr, x=df_galia_gr['galia50'], y=df_galia_gr['price'])
ax.set_xlabel('Galia kW')
ax.set_ylabel('Kaina')
st.pyplot(fig, use_container_width=True)



st.header('Kainos priklausomybė nuo automobilio pavarų dėžės ir kėbulo tipo ')

df_tipas = df[(df['PavaruDeze'] != 'None')][['PavaruDeze', 'KebuloTipas', 'price']]
df_tipas_gr = df_tipas.groupby(['PavaruDeze', 'KebuloTipas']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_tipas_gr, x='PavaruDeze', y='price', hue='KebuloTipas')

# ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)


st.pyplot(fig, use_container_width=True)