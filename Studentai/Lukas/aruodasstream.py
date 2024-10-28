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


SDB = sqlite3.connect('aruodas.db')
Cs = SDB.cursor()

sql="""select * from Aruodas;"""
df_with_dubs = pd.read_sql_query(sql, con=SDB)
df = df_with_dubs.drop_duplicates()

miestai = ['Vilnius', 'Kaunas', 'Klaipėda', 'Palanga', 'Panevėžys']

def plotas(x):
    # if 'm²' in x:
    if x is not None:
        return float(x.replace(' m²', '',).replace(',', '.'))
    else:
        return np.nan
    
df['plotas'] = df['Plotas:'].apply(plotas)
df['plotas5'] = df[df['plotas'] != None]['plotas'].apply(lambda x: float(np.ceil(x/5) * 5))

#############################################################################
st.header('Vidutinis būtų plotas 5-iuose mietuose')

df_plotas = df[df['miestas'].isin(miestai)][['miestas', 'plotas']]
df_plotas_gr = df_plotas.groupby('miestas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=df_plotas_gr, x='miestas', y='plotas')
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig, use_container_width=True)

######################################################
st.header('Butų pasisirstymas pagal plotą')

df_vln = df[df['miestas'] == 'Vilnius'].groupby(['plotas5']).size().reset_index(name='Count')
df_kns = df[df['miestas'] == 'Kaunas'].groupby(['plotas5']).size().reset_index(name='Count')
df_klp = df[df['miestas'] == 'Klaipėda'].groupby(['plotas5']).size().reset_index(name='Count')
df_pal = df[df['miestas'] == 'Palanga'].groupby(['plotas5']).size().reset_index(name='Count')
df_pan = df[df['miestas'] == 'Panavėžys'].groupby(['plotas5']).size().reset_index(name='Count')

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1,figsize=(8, 20))

sns.barplot(data=df_vln, x='plotas5', y='Count', ax=ax1)
ax1.tick_params(axis='x', rotation=90, labelsize=8)
ax1.set_ylabel('Butų kiekis')
ax1.set_xlabel('plotas')
ax1.set_title('Vilniaus būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_kns, x='plotas5', y='Count', ax=ax2)
ax2.tick_params(axis='x', rotation=90, labelsize=8)
ax2.set_ylabel('Butų kiekis')
ax2.set_xlabel('plotas')
ax2.set_title('Kauno būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_klp, x='plotas5', y='Count', ax=ax3)
ax3.tick_params(axis='x', rotation=90, labelsize=8)
ax3.set_ylabel('Butų kiekis')
ax3.set_xlabel('plotas')
ax3.set_title('Klaipėdos būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_pal, x='plotas5', y='Count', ax=ax4)
ax4.tick_params(axis='x', rotation=90, labelsize=8)
ax4.set_ylabel('Butų kiekis')
ax4.set_xlabel('plotas')
ax4.set_title('Palangos būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_pal, x='plotas5', y='Count', ax=ax5)
ax5.tick_params(axis='x', rotation=90, labelsize=8)
ax5.set_ylabel('Butų kiekis')
ax5.set_xlabel('plotas')
ax5.set_title('Panevėžio būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)


fig.tight_layout()
st.pyplot(fig, use_container_width=True)