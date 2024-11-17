import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
# import plotly.express as px
import numpy.polynomial.polynomial as poly
import streamlit as st
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')


def make_dataframe():
    SDB = sqlite3.connect('../../DATA/WEBscr.db')
    C = SDB.cursor()

    sql1="""select * from TAutos;"""
    df1 = pd.read_sql_query(sql1, con=SDB)

    sql2="""select * from TUrl;"""
    df2 = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    
    df_with_dubs = pd.merge(df1, df2, on='id', how='inner')
    df = df_with_dubs.drop_duplicates()
    return df


# susikuriam dataframem
df = make_dataframe()


# tvarkome duomenis
def get_kaina(x):
    kaina = x.split(';')[-1].split('\n')[0].replace(' ', '').replace('€', '')
    return int(kaina)

df['kaina'] = df['params'].apply(get_kaina)

def amzius(x):
    if x != None:
        return int(2024 - int(x[:4]))
    
df['amzius'] = df['Pirma registracija'].apply(amzius)

def rida(x):
    if x != None:
        return int(x.replace(' ', '').replace('km', ''))
    else:
        return np.nan
    
df['rida'] = df['Rida'].apply(rida)


def galia(x):
    if x != None:
        if 'kW' in x:
            return int(x.split('(')[-1][:-3])
    else:
        return np.nan

df['galia'] = df['Variklis'].apply(galia)    

def baterija(x):
    if x != None:
        return int(x.replace(' ', '').replace('kWh', ''))
    
df['baterija'] = df['Baterijos talpa, kWh'].apply(baterija)  


def eatstumas(x):
    if x != None:
        return int(x.replace(' ', '').replace('km', ''))
    
df['eatstumas'] = df['Elektra nuvažiuojamas atstumas'].apply(eatstumas)

df['R5000'] = df[df['rida'] != None]['rida'].apply(lambda x: float(np.ceil(x/5000) * 5000))
df['ea50'] = df[df['eatstumas'] != None]['eatstumas'].apply(lambda x: float(np.ceil(x/50) * 50))


# duomenys filtrams
gamintojai_kiekiai =df['gamintojas'].value_counts()
g = gamintojai_kiekiai[gamintojai_kiekiai.values >= 10]
gamintojai = ['--pasirinkite--'] + sorted(list(g.index))

kuro_tipai = ['--pasirinkite--'] + sorted(list(set(df['Kuro tipas'].tolist()))) 

pavaros = ['--pasirinkite--'] + ['Mechaninė', 'Automatinė']

kebulo_tipai = ['--pasirinkite--'] + sorted(list(set(df[df['Kėbulo tipas'].notna()]['Kėbulo tipas'].tolist())))

my_list = list(range(2024, 1927, -1))
metai = ['--pasirinkite--'] + my_list

# Vartotojo pasirinkimai
selected_gamintojas = st.selectbox('Pasirinkite gamintoją:', gamintojai)
selected_metai = st.selectbox('Pasirinkite automobilio pagaminimo metus', metai)
selected_rida = st.slider("Pasirinkite automobilio ridą:", min_value=0, max_value=500000, step=1000)
selected_kuras =st.selectbox('Pasirinkite kuro tipą', kuro_tipai)
selected_pavara = st.selectbox('Pasirinkite pavarų dėžę', pavaros)
selected_kebulas = st.selectbox('Pasirinkite kėbulo tipą', kebulo_tipai)


if isinstance(selected_metai, int):
    selected_amz = 2024 - selected_metai



# Create a button in Streamlit
if st.button('Ieškoti'):
    # kai nuspaudžiamas mygtukas
    st.write(f"Pasirinktas gamintojas: {selected_gamintojas}, automobilio amžius: {selected_amz}, rida: {selected_rida}") 
    
    df_rida = df[df['gamintojas'] == selected_gamintojas][['kaina', 'R5000']]
    df_rida.dropna(inplace=True)
    df_rida_gr = df_rida.groupby('R5000').mean(numeric_only=True).reset_index()

    df_rida_gr2 = df_rida_gr[df_rida_gr['R5000'] < 500000]

    fig, axis = plt.subplots(figsize=(8, 4.5))
    sns.regplot(data=df_rida_gr2, x='R5000', y='kaina', order=3)
    # axis.axhline(y=0)
    st.pyplot(fig)
    



