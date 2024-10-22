import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
conn = sqlite3.connect('cars1.db')
df = pd.read_sql_query("SELECT * FROM car_listings", conn)
conn.close()
df = df.drop_duplicates()

def clean_and_convert(column, unit):
    return pd.to_numeric(
        df[column].str.replace(unit, '', regex=True).str.replace(' ', ''), 
        errors='coerce'
    )


df['price'] = clean_and_convert('price', '€')
df['mileage'] = clean_and_convert('mileage', 'km')


df = df.dropna(subset=['price', 'mileage'])


st.title("Car Listings Analysis")
st.dataframe(df)


st.subheader("Price vs Mileage Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(df['price'], df['mileage'], alpha=0.5)
ax.set_title('Price vs Mileage')
ax.set_xlabel('Mileage (km)')
ax.set_ylabel('Price (€)')
st.pyplot(fig)