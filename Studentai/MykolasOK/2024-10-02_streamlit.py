import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart',page_title='DEMO STREAMLIT MAP',layout='centered')

st.header('Web bandymas - streamlit žemėlapis')
st.header('Pirmoji tema')

a=np.arange(1,11)
b=np.random.randint(1,11,10)
c=np.random.randint(1,11,10)*a
fig,ax=plt.subplots()
ax.plot(a,b,color="Green",linewidth=3)
ax.bar(a,c,color="xkcd:browny orange")
# st.pyplot(fig)

a=np.arange(1,11)
b=np.random.randint(1,11,10)
c=np.random.randint(1,11,10)*a
figa,axa=plt.subplots()
axa.plot(a,b,color="Blue",linewidth=3)
axa.bar(a,c,color="xkcd:yellow")
# st.pyplot(figa)

tekstas=st.text_input(label="Įrašykite")
if tekstas :
    st.write("Jūs įvedėte:",tekstas)

left,right=st.columns(2)
left.write("left.write")
left.pyplot(fig)
right.write("right.write")
right.pyplot(figa)

st.write("Nuo 'st.write' baigiasi du stulpeliai")

# st.header('Antroji tema') 

# def read_json(name):
#     df = pd.read_json(name)
#     return df
 
# @st.cache_data
# def read_json_cached(namea):
#     dff = pd.read_json(namea)
#     return dff

# left,right = st.columns(2)
 
# file = left.file_uploader(label='Nurodykite JSON failą (left)')
# left.write('paprasta funkcija')
# if file is not None:
#     dfa = read_json(file)
#     left.write(dfa.head(5))

# file = right.file_uploader(label='Nurodykite JSON failą (right)')
# right.write('dekoruota funkcija')
# if file is not None:
#     dfb = read_json_cached(file)
#     right.write(dfb.head(5))

st.header('Trečioji tema') 

f = st.file_uploader(label='DATA/GMP.csv')
if f is not None:
    df = pd.read_csv(f)
    gaisrai = df[df['zemesnis_ivykio_tipas'].str.contains('Gaisr',na=False)]
    ket = df[df['zemesnis_ivykio_tipas'].str.contains('KET',na=False)]

    fig = px.scatter_mapbox(data_frame=gaisrai,lon='X',lat='Y',zoom=7) # ,color='spalva'
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)
# Žr. https://stackoverflow.com/questions/64527823/plotly-express-plot-scatter-mapbox-with-feature-colors-from-dataframe-column-p

st.header('Ketvirtoji tema - N.D. užduotis') 

# N.D. užduotis:
# žr. apply() axis
# nuskaityti GMP failą (didenįjį), x, y koordinantes konvertuoti į pasaulines ilgumą ir platumą, pridėti gautąsias koordinantes kaip du naujus stulpelius.
# atrinkti tik gaisrus iki 3jų autocisternų ir jų įvykių vietas atvaizduoti plotly express mapbox grafike.
# galite tai atlikti arba jupyter notebooke arba galite panaudoti streamlit skriptą
# https://stackoverflow.com/questions/30026815/add-multiple-columns-to-pandas-dataframe-from-function

