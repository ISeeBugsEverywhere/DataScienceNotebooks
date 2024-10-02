import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart',page_title='DEMO STREAMLIT MAP',layout='centered')

st.header('Pirmasis web bandymas - streamlit žemėlapis')
a=np.arange(1,11)
b=np.random.randint(1,11,10)
c=np.random.randint(1,11,10)*a
fig,ax=plt.subplots()
ax.plot(a,b,color="Green",linewidth=3)
ax.bar(a,c,color="xkcd:browny orange")
st.pyplot(fig)

tekstas=st.text_input(label="Įrašykite")
if tekstas :
    st.write("Jūs įvedėte:",tekstas)