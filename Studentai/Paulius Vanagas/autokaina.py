import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os
import sqlite3
import seaborn as sns
import numpy.polynomial.polynomial as poly

import streamlit as st
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='wide')

def duomenys():
    SDB = sqlite3.connect(r'C:\Users\pauli\Desktop\DataScienceNotebooks\DATA\WEBscr.db')
    Cs = SDB.cursor()
    sql="""SELECT * FROM TUrl;"""
    Cs.execute(sql)
    ans = Cs.fetchall()
    df1 = pd.read_sql_query(sql, con=SDB)

    df1['kaina']= df1['params'].apply(lambda x: str(x.split(';')[-1]))
    df1['kaina']= df1['kaina'].apply(lambda x: str(x.split('€')[0]).replace(' ','').replace('€',''))
    df1['kaina']= df1['kaina'].apply(lambda x: float(x))

    df1['metai']=df1['params'].apply(lambda x: str(x.split(';')[1]))
    df1['metai']=df1['metai'].apply(lambda x: int(x.split('-')[0]))

    df1['rida']=df1['params'].apply(lambda x: str(x.split(';')[-3]))

    SDB = sqlite3.connect(r'C:\Users\pauli\Desktop\DataScienceNotebooks\DATA\WEBscr.db')
    Cs = SDB.cursor()
    sql="""SELECT * FROM TAutos;"""
    Cs.execute(sql)
    ans = Cs.fetchall()
    df2 = pd.read_sql_query(sql, con=SDB)

    df1=df1[['id','kaina']]
    df= pd.merge(df2, df1, on='id', how='inner')

    df=df[['gamintojas', 'Pirma registracija', 'Kuro tipas', 'Pavarų dėžė', 'Rida', 'Defektai', 'kaina', 'Kėbulo tipas' ]]
    
    return df

def sutvarko_duomenis(df):

    df = df[df['Pirma registracija'].notna()]
    # df = df[df['Pavarų dėžė'].notna()]
    df = df[df['Rida'].notna()]
    df = df[df['Kėbulo tipas'].notna()]
    df = df[df['Defektai'].isna()]
    df= df[df['kaina'] <100000]
    df=df[['gamintojas', 'Pirma registracija', 'Kuro tipas', 'Pavarų dėžė', 'Rida', 'kaina', 'Kėbulo tipas' ]]

    df['Pirma registracija']= df['Pirma registracija'].apply(lambda x: float(str(x).split('-')[0]))
    # df.loc[:, 'Pirma registracija'] = df['Pirma registracija'].apply(lambda x: int(str(x).split('-')[0]).strip())
    df= df[df['Pirma registracija'] > 1990]

    df['Rida']= df['Rida'].apply(lambda x: float(str(x).replace(' ','').replace('km','')))
    df= df[df['Rida'] <500000]
    
    return df

def get_gamintojas(df):
    dftop = df.groupby('gamintojas').count()
    dftop = dftop.sort_values(by='kaina', ascending=False)
    dftop = dftop.head(7)
    top7 = dftop.index.to_list()
    gamintojas = st.selectbox('Pasirinkite gamintoją:', top7)
    df1=df[df['gamintojas']==gamintojas]
    st.write('palyginamų automobilių kiekis ', len(df1))
    return gamintojas, df1

def get_kuras(df1):
    kuras=df1['Kuro tipas'].unique()
    kuras1 = st.selectbox('Pasirinkite kuro tipą:', kuras)
    df1=df1[df1['Kuro tipas']==kuras1]
    st.write('palyginamų automobilių kiekis ', len(df1))
    return kuras1, df1

def get_pavaros(df1):
    pavaros=df1['Pavarų dėžė'].unique()
    pavaros1 = st.selectbox('Pasirinkite pavarų tipą:', pavaros)
    df1=df1[df1['Pavarų dėžė']==pavaros1]
    st.write('palyginamų automobilių kiekis ', len(df1))
    return pavaros1, df1

def get_metai(df1):
    metai = st.number_input("Įveskite pagaminimo metus nuo 1991 iki 2024", min_value=1991, max_value=2024, step=1)
    df1 = df1[(df1['Pirma registracija'] >= (metai - 1)) & (df1['Pirma registracija'] <= (metai + 1))]
    st.write('palyginamų automobilių kiekis ', len(df1))
    return metai, df1

def get_kebulas(df1):
    kebulas=df1['Kėbulo tipas'].unique()
    kebulas1=st.selectbox('Pasirinkite kėbulą:', kebulas)
    df1=df1[df1['Kėbulo tipas']==kebulas1]
    st.write('palyginamų automobilių kiekis ', len(df1))
    return kebulas1, df1

def get_rida():
    rida = st.number_input("Įveskite ridą nuo 0 iki 500000", min_value=0, max_value=500000, step=1)
    return rida

def kainos_ivertinimas(df1, pasirinkimai):

    # coef = np.polyfit(x=df1['Rida'], y=df1['kaina'], deg=4)
    # fn_fit = poly.Polynomial(coef[::-1])
    # kainos_fitted = fn_fit(df1['Rida'])
    # df1['K_fit'] = kainos_fitted
    
    coefs = np.polyfit(x=df1['Rida'], y=np.log(df1['kaina']), deg=1)
    #!coefs are in decreasing order!↪
    B,A = coefs
    yfit = np.exp(A)*np.exp(B*pasirinkimai['rida'])+1
    
    # fig, ax = plt.subplots()
    # ax = sns.regplot(data=df1, x='Rida', y='kaina', order=2)
    # ax.scatter(x=df1['Rida'][::10], y=df1['K_fit'][::10], c='red')

    # st.pyplot(fig)
    
    
    ats = round((yfit), 0)
    
    if ats <= 0:
        ats= 'Teks vežti į metalo laužą'
    
    return ats
    

df = duomenys()
df = sutvarko_duomenis(df)

pasirinkimai= {'gamintojas': None, 'pavaros': None, 'metai': None, 'kebulas': None, 'rida': None, 'kuras': None}

pasirinkimai['gamintojas'], df1 = get_gamintojas(df)
pasirinkimai['kuras'], df1 = get_kuras(df1)

if pasirinkimai['kuras'] != 'Elektra':
    pasirinkimai['pavaros'], df1 = get_pavaros(df1)
pasirinkimai['metai'], df1 = get_metai(df1)
pasirinkimai['kebulas'], df1= get_kebulas(df1)
pasirinkimai['rida'] = get_rida()
galima_kaina = kainos_ivertinimas(df1, pasirinkimai)

st.write("You entered:", pasirinkimai['gamintojas'], pasirinkimai['kuras'], pasirinkimai['pavaros'], pasirinkimai['metai'], pasirinkimai['kebulas'], pasirinkimai['rida'])
st.write('numanoma kaina: ', galima_kaina)
st.write('palyginamų automobilių kiekis ', len(df1))