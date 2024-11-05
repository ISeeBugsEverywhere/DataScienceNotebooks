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

SDB = sqlite3.connect('Auto.db')
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

st.header('Ar Tech. apžiūros turėjimas daro įtaka kainai? ')

def TA(x):
    if x != 'None':
        return 'Galioja'
    else:
        return 'Negalioja'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
df['TA'] = df['TechApžiuraIki'].apply(TA)

df[(df['PavaruDeze'] != 'None')].groupby(['PavaruDeze','TA'])['price'].mean(numeric_only=True).unstack().plot(kind='bar' , legend=True, xlabel='Tech. apžiūra', ax=ax1)
df.groupby('TA')['price'].count().plot(kind='bar' , ylabel='Kiekis', xlabel='Tech. apžiūra', ax=ax2)
st.pyplot(fig)



st.header('Importuoti automobiliai ')

salys = df[df['PirmosiosRegistracijosSalis'] != 'None']['PirmosiosRegistracijosSalis'].value_counts()

df_salys = df[(df['PirmosiosRegistracijosSalis'] != 'None')&(df['PavaruDeze'] !='None')][['PirmosiosRegistracijosSalis', 'PavaruDeze', 'price']]

df_salys_gr = df_salys.groupby(['PirmosiosRegistracijosSalis', 'PavaruDeze']).mean(numeric_only=True)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

B1 = ax1.bar(salys.index, salys.values)
ax1.bar_label(B1)
ax1.tick_params(axis='x', rotation=45)
ax1.set_ylabel('Automobilių kiekis')
ax1.set_title('Iš kur atvežti automobiliai')

sns.barplot(data=df_salys_gr, x='PirmosiosRegistracijosSalis', y='price', hue='PavaruDeze', ax=ax2)
ax2.tick_params(axis='x', rotation=45)
ax2.set_title('Vidutinės kainos')

fig.tight_layout()
st.pyplot(fig, use_container_width=True)



st.header('Top 10 gamintojų')
# Kodėl gaunu blogai per streamlit?
gamintojai = df['Marke'].value_counts()
top10g = gamintojai.head(10).index.to_list()
df_top = df[df['Marke'].isin(top10g)]
top_gamintojai = df_top['Marke'].value_counts()

fig, ax1 = plt.subplots(figsize=(8, 4.5))

B1 = ax1.bar(top_gamintojai.index, top_gamintojai.values)
ax1.bar_label(B1)
ax1.tick_params(axis='x', rotation=90)
plt.title('TOP 10 gamintojai')


st.pyplot(fig)




st.header('Top 10 gamintojų kainos priklausomybė nuo ridos')

fig, axis = plt.subplots()
df_top_gamintojai = df[df['Marke'].isin(top10g)][['Marke', 'R5000', 'price']]

df_top_gamintojai_gr = df_top_gamintojai.groupby(['Marke', 'R5000']).mean(numeric_only=True)

sns.scatterplot(data=df_top_gamintojai_gr, x='R5000', y='price', hue='Marke', ax=axis)
st.pyplot(fig, use_container_width=True)






st.header('Automobilių pasiskirstymas pagal kuro rūšį')
kuras = df['Kuras'].value_counts()
fig, ax1 = plt.subplots(figsize=(8, 4.5))
B1 = ax1.bar(kuras.index, kuras.values)
ax1.bar_label(B1)
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig, use_container_width=True)



st.header('Top 10 gamintojų kainos priklausomybė nuo amžiaus')
fig, axis = plt.subplots()
df_top_amz = df[df['Marke'].isin(top10g)][['Marke', 'amzius', 'price']]

df_top_amz_gr = df_top_amz.groupby(['Marke', 'amzius']).mean(numeric_only=True)

sns.scatterplot(data=df_top_amz_gr, x='amzius', y='price', hue='Marke')
st.pyplot(fig, use_container_width=True)



st.header('Top 10 gamintojų automobilių galios pasiskirstymas')
df_x = df[(df['Marke'].isin(top10g)) & (df['galia'] != 'None')]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'Marke', y='galia', showmeans=True, showfliers=False)
axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Markė',ylabel='Galingumas')
# for container in ax.containers:
#     ax.bar_label(container)
axes.legend()
st.pyplot(fig, use_container_width=True)




st.header('Top 10 gamintojų automobilių ridos pasiskirstymas')
df_x = df[(df['Marke'].isin(top10g)) & (df['rid'] != 'None')]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'Marke', y='rid', showmeans=True, showfliers=False)
axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Markė',ylabel='Rida')
# for container in ax.containers:
#     ax.bar_label(container)
axes.legend()
st.pyplot(fig, use_container_width=True)



st.header('Top 10 gamintojų automobilių amžiaus pasiskirstymas')
df_x = df[(df['Marke'].isin(top10g)) & (df['amzius'] != 'None')]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'Marke', y='amzius', showmeans=True, showfliers=False)
axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Markė',ylabel='Amžius')
# for container in ax.containers:
#     ax.bar_label(container)
axes.legend()
st.pyplot(fig, use_container_width=True)


st.header('Defektai')

fig, ax = plt.subplots()

df_defektai = df[(df['Defektai'] != 'None')][['Defektai', 'Marke']]
df_defektai.groupby(['Defektai'])['Marke'].count().plot(kind='bar')
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig)


st.header('Automobiliai su Defektais')

fig, ax = plt.subplots()

df_defektai = df[(df['Defektai'] != 'None')][['Defektai', 'Marke']]
df_defektai.groupby(['Marke'])['Defektai'].count().plot(kind='bar')
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig)


st.header('EV')

fig, ax = plt.subplots()

df_elektra = df[(df['Kuras'] == 'Elektra')][['Kuras', 'Marke']]
df_elektra.groupby(['Marke'])['Kuras'].count().plot(kind='bar')
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig)


st.header('EV kainos')

fig, ax = plt.subplots()

df_elektra = df[(df['Kuras'] == 'Elektra')][['Kuras', 'Marke', 'price']]
df_elektra.groupby(['Marke'])['price'].mean(numeric_only=True).plot(kind='bar')
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig)


st.header('EV kainos nuo amžiaus (Tesla)')

fig, ax = plt.subplots()

df_elektra = df[(df['Kuras'] == 'Elektra')& (df['Marke'] == 'Tesla')][['amzius', 'Marke', 'price']]
df_elektra.groupby(['amzius'])['price'].mean(numeric_only=True).plot(kind='line')
# for container in ax.containers:
#     ax.bar_label(container)
st.pyplot(fig)

st.header('EV kainos ridos (Tesla)')

fig, ax = plt.subplots()

df_elektra = df[(df['Kuras'] == 'Elektra') & (df['Marke'] == 'Tesla')][['R5000', 'Marke', 'price']]
df_elektra.groupby(['R5000'])['price'].mean(numeric_only=True).plot(kind='line')
# for container in ax.containers:
#     ax.bar_label(container)
st.pyplot(fig)



st.header('EV kainos ridos (Tesla)')
#  skaidyti per du grupavimus, paskui reikia pastumti stulpelius
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

df_elektra = df[(df['Kuras'] == 'Elektra') & (df['Marke'] == 'Tesla')][['rid','amzius', 'Marke', 'price']]
df_elektra.groupby(['amzius'])[['rid', 'price']].mean().plot(kind='bar', ax=ax1)
for container in ax1.containers:
    ax1.bar_label(container)
# st.pyplot(fig)
plt.show()
st.pyplot(fig)