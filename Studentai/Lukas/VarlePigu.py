import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
# import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import sqlite3



#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')

st.header('Šaldytuvai')

SDB = sqlite3.connect('VarlePigu.db')
Cs = SDB.cursor()
sql="""SELECT kaina, `montavimo tipas`
FROM "SaldytuvaiVarle";
"""
df = pd.read_sql_query(sql, con=SDB)
SDB.close()
df.dropna(subset='montavimo tipas', inplace=True)

def set_saldytuvo_tipas(x):
    if 'stat' in x:
        return 'Laivai pastatomi'
    elif 'montuo' in x:
        return 'Įmontuojami'
    elif 'ntegruo' in x:
        return 'Integruojami'
    else:
        return 'Kita'
    
df['mtipas'] =df['montavimo tipas'].apply(set_saldytuvo_tipas)
df['kaina'] = df['kaina'].apply(lambda x: float(x))

c =df['mtipas'].value_counts()
fig, (axis1, axis2) = plt.subplots(1,2, figsize=(10.5, 4.5))
axis1.pie(c.values, labels=c.index, autopct='%.2f%%')
sns.boxplot(data=df, x='mtipas', y='kaina', showmeans=True, showfliers=False, ax=axis2)
axis1.set_title('Šaldytuvų pasiskirstymas pagal montavimo tipą (Varle.lt)')
axis2.set_title('Kainų pasiskirstymas pagal šaldytuvų  montavimo tipą (Varle.lt)')
axis2.set_xlabel('Tipas')
axis2.set_ylabel('Kaina')
fig.tight_layout()
st.pyplot(fig, use_container_width=True)