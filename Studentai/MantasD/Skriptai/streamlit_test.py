import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('Mano pirmasis Data Science puslapis')

A = np.arange(1,11)
B = np.random.randint(1,11,10)
C = np.random.randint(1,11,10)*A

fig, ax = plt.subplots()
ax.plot(A,B, zorder = 2)
ax.bar(A,C, zorder = 1)

st.pyplot(fig, use_container_width=True)

left, right = st.columns(2)

left.header('Čia yra kairė')
left.pyplot(fig)

right.header('Čia yra dešinė')
right.pyplot(fig)

st.write("Nuo čia baigiasi du stulpeliai")

left.write('Kažko svarbi informacija')

tekstas = st.text_input(label= 'Prašome įrašyti informaciją')

if tekstas:
    st.write("Jūs įvedėte", tekstas)

def read_json(name):
    df = pd.read_json(name)
    return df

@st.cache_data
def read_json_cached(name):
    df = pd.read_json(name)
    return df
left, right = st.columns(2)   

file = left.file_uploader(label="Čia galite nurodyti JSON failą left")

left.write('Paprasta funkcija')
if file is not None:
    df = read_json(file)
    left.write(df.head(5))
    
file = right.file_uploader(label="Čia galite nurodyti JSON failą right")  
  
right.write('Dekoruota funkcija')
if file is not None:
    df = read_json_cached(file)
    right.write(df.head(5))
