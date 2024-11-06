import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('aruodas.db')
df = pd.read_sql_query("SELECT * FROM listings", conn)
conn.close()
df = df.drop_duplicates()



df['City'] = df['address'].str.split(',').str[0]
df['plotasI'] = df['plotas'].replace('N/A', np.nan)
df['plotasI'] = df['plotasI'].str.replace(' m²', '').str.replace(',', '.').astype(float)
df['plotas_rounded'] = df['plotasI'].round(-1)

cities = ['Vilnius', 'Kaunas', 'Klaipėda', 'Palanga', 'Panevėžys']
df_f = df[df['City'].isin(cities)]

mean_area = df_f.groupby('City')['plotas_rounded'].mean().reset_index()

mode_area = df_f.groupby('City')['plotas_rounded'].agg(lambda x: x.mode()[0]).reset_index()

fig, ax = plt.subplots()


ax.bar(mean_area['City'], mean_area['plotas_rounded'], color='skyblue', label='Mean Area')


ax.set_xlabel('City')
ax.set_ylabel('Area (m²)')
ax.set_title('Average and Most Common Property Sizes by City')


# print(df.head())

st.pyplot(fig)


st.write('Mean Area by City:')
st.write(mean_area)

st.write('Most Common Area by City:')
st.write(mode_area)

from datetime import datetime


conn_sale = sqlite3.connect('aruodas.db')

conn_rent = sqlite3.connect('aruodas_rent.db')


df_sale = pd.read_sql_query("SELECT * FROM listings", conn_sale)
df_rent = pd.read_sql_query("SELECT * FROM listings", conn_rent)


df_sale['listing_type'] = 'sale'
df_rent['listing_type'] = 'rent'

df = pd.concat([df_sale, df_rent], ignore_index=True)


df['metaiI'] = pd.to_numeric(df['metai'].replace('N/A', np.nan))

now = datetime.now().year

df['amzius'] = now - df['metaiI']

mean_age = df.groupby('listing_type')['amzius'].mean().reset_index()

print("Average age of properties by listing type (sale or rent):")
print(mean_age)

fig, ax = plt.subplots()
ax.bar(mean_age['listing_type'], mean_age['amzius'], color=['blue', 'orange'])
ax.set_xlabel('Listing Type')
ax.set_ylabel('Average Age of Property (years)')
ax.set_title('Average Age of Sale vs Rental Properties')

st.pyplot(fig)

st.write("Mean age of properties by listing type (sale or rent):")
st.write(mean_age)

conn_sale.close()
conn_rent.close()


df['price'] = df['price'].str.replace('€', '').str.replace(' ', '').astype(float)

df['energijos_klase'] = df['energijos_klase'].replace('N/A', np.nan)

avg_price = df.groupby('energijos_klase')['price'].mean().reset_index()

fig, ax = plt.subplots()
ax.bar(avg_price['energijos_klase'], avg_price['price'], color='skyblue')
ax.set_xlabel('Energy Class')
ax.set_ylabel('Average Price (€)')
ax.set_title('Average Price by Energy Class')

st.pyplot(fig)

st.write("Average price by energy class:")
st.write(avg_price)

df['City'] = df['address'].str.split(',').str[0]
# df['price'] = df['price'].str.replace('€', '').str.replace(' ', '').astype(float)
cities = ['Vilnius', 'Kaunas', 'Klaipėda', 'Palanga', 'Panevėžys']
df_f = df[df['City'].isin(cities)]

grouped = df_f.groupby(['City', 'sildymas'])['price']

fig, ax = plt.subplots()
df_f.boxplot(column='price', by='City', ax=ax, showfliers=False, showmeans=True)

ax.set_title('Price Distribution by City')
ax.set_xlabel('City')
ax.set_ylabel('Price (€)')
plt.suptitle('')

st.pyplot(fig)

st.write("Price data by heating type and city:")
st.write(df_f)


avg_priceI = df_f.groupby('sildymas')['price'].mean().reset_index()
fig, ax = plt.subplots()
ax.bar(avg_priceI['sildymas'], avg_priceI['price'], color='skyblue')
ax.set_xlabel('Heating Type')
ax.set_ylabel('Average Price (€)')
ax.set_title('Average Price by Heating Type')

st.pyplot(fig)

st.write("Average price by Heating Type:")
st.write(avg_priceI)


avg_priceI = df.groupby('pastato_tipas')['price'].mean().reset_index()
avg_age = df.groupby('pastato_tipas')['amzius'].mean().reset_index()

md = pd.merge(avg_priceI, avg_age, on='pastato_tipas')

fig, ax = plt.subplots()
for building_type in df['pastato_tipas'].unique():
    subset = df[df['pastato_tipas'] == building_type]
    ax.scatter(subset['amzius'], subset['price'], label=building_type)

ax.set_xlabel('Building Age (years)')
ax.set_ylabel('Price (€)')
ax.set_title('Relationship between Price and Building Age by Building Type')
ax.legend(title='Building Type')

st.pyplot(fig)

st.write("Average price and age by building type:")
st.write(md)


fig, ax = plt.subplots()

scatter = ax.scatter(df['aukstas'], df['price'], c=df['aukstu_sk'], cmap='viridis', alpha=0.8)

colorbar = fig.colorbar(scatter, ax=ax, label='Total Building Floors')
colorbar.set_label('Total Floors in Building')

ax.set_xlabel('Apartment Floor (aukstas)')
ax.set_ylabel('Price (€)')
ax.set_title('Relationship between Price, Apartment Floor, and Building Height')

st.pyplot(fig)

st.write("Data on price, apartment floor, and total building height:")
st.write(df)





