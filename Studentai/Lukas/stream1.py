# import streamlit as st
# #streamlit page config:
# st.set_page_config(page_icon=':bar_chart', page_title='DEMO',layout='wide', initial_sidebar_state="collapsed")
# st.title(":bar_chart: StreamLit demo projektas :shark:")
# st.header(":chart_with_upwards_trend: :flag-lt:")
# # sidebar:
# sidebar = st.sidebar
# sidebar.header("Šoninė juosta")

# mysql-connector-python==8.0.29

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('Mano pirmas data science web puslapis')

A = np.arange(1, 11)
B = np.random.randint(1, 11, 10)
C = np.random.randint(1, 11, 10)*A

fig, ax = plt.subplots()

ax.plot(A, B, zorder=2, color ='xkcd:deep green')
ax.bar(A, C, zorder=1)

st.pyplot(fig, use_container_width=True)

# left, center, right = st.columns(3)
left, right = st.columns(2)

left.header('Čia yra kairė')
left.pyplot(fig)

# center.header('Čia yra center')
# center.pyplot(fig)

right.header('Čia yra dešinė')
right.pyplot(fig)

st.write("Nuo čia baigiasi du stulpeliai")

tektas = st.text_input(label='prasome irasyti teksta')

if tektas:
    st.write('jus ivedete:', tektas)
    
    
file = st.file_uploader(label='cia galite nurodyti faila')
if file is not None:
    df = pd.read_csv(file)
    st.write(df.head(5))
    

def read_json(name):
    df = pd.read_json(name)
    return df

@st.cache_data
def read_json_cached(namea):
    dff = pd.read_json(namea)
    return dff

left, right = st.columns(2)

file = left.file_uploader(label='Nurodykite JSON failą (left)')


left.write('paprasta funkcija')
if file is not None:
    dfa = read_json(file)
    left.write(dfa.head(5))
    
file = right.file_uploader(label='Nurodykite JSON failą (right)')
right.write('dekoruota funkcija')
if file is not None:
    dfb = read_json_cached(file)
    right.write(dfb.head(5))
    
st.header('Kita dalis!')