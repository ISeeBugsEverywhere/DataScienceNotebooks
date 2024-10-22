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
B = np.random.randint(1,11,10)* A
C = np.random.randint(1,11,10)
fig, ax = plt.subplots()
ax.plot(A, B, zorder=2)
ax.bar(A,C , zorder= 1)
st.pyplot(fig, use_container_width = True)

left, right = st.columns(2)

left.header('Cia yra kaire')
left.pyplot(fig)

right.header('Cia yra desine')
right.pyplot(fig)

# st.write('Nuo cia bigiasi du stulpeliai')

# left.write('Cia svarbi info')

# tekstas = st.text_input(label= 'Info')
# if tekstas:
#     st.write('Jus ivedete', tekstas)

# file = st.file_uploader(label = 'cia galite nurodity faila')
# if file is not None:
#     df = pd.read_csv(file)
#     st.write(df.head(5))


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('Mano pirmas data science web puslapis')

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


f = st.file_uploader(label='CSV')
if f is not None:
    df = pd.read_csv(f)
    fig = px.scatter_mapbox(data_frame=df, lon='X', lat='Y', zoom=5)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)