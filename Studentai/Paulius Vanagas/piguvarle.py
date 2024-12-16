import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
import plotly.express as px
from datetime import datetime, timedelta
import os


st.set_page_config(page_icon=':bar_chart', page_title='pigu ir varle', layout='centered')
options = ['Šaldytuvai','Dronai','Planšetiniai kompiuteriai','Televizoriai','Dviračiai']
selected_option = st.selectbox('Pasirinkite prekių kategoriją:', options)

if selected_option == 'Šaldytuvai':
    DB = sqlite3.connect('varlesaldytuvai.db')
    C = DB.cursor()
    sql="""SELECT * FROM saldytuvai;"""
    dfv = pd.read_sql_query(sql, con=DB)
    dfv['kaina']=dfv['kaina'].astype(float)
    
    DB = sqlite3.connect('pigusaldytuvai.db')
    C = DB.cursor()
    sql="""SELECT * FROM saldytuvai;"""
    dfp = pd.read_sql_query(sql, con=DB)
    dfp = dfp.dropna(subset=['kaina'])
    dfp['kaina'] = dfp['kaina'].apply(lambda x: str(x).replace(' ', ''))
    dfp['kaina']=dfp['kaina'].astype(float)
    
    dfv1=dfv
    dfv1['kaina']=dfv1['kaina'].astype(float)
    dfv1 = dfv1.dropna(subset=['montavimo tipas'])
    dfv1['montavimo tipas'] = dfv1['montavimo tipas'].apply(lambda x: str(x).replace('laisvai pastatoma', 'laisvai pastatomas'))
    dfv1['montavimo tipas'] = dfv1['montavimo tipas'].apply(lambda x: str(x).replace('laisvai pastatomos', 'laisvai pastatomas'))
    dfv1['montavimo tipas'] = dfv1['montavimo tipas'].apply(lambda x: str(x).replace('laisvai statomi', 'laisvai pastatomas'))
    dfv1['montavimo tipas'] = dfv1['montavimo tipas'].apply(lambda x: str(x).replace('pastatytas', 'laisvai pastatomas'))
    dfv1['montavimo tipas'] = dfv1['montavimo tipas'].apply(lambda x: str(x).replace('įmontuojami', 'laikinas'))
    dfv1['montavimo tipas'] = dfv1['montavimo tipas'].apply(lambda x: str(x).replace('montuojami', 'įmontuojamas'))
    dfv1['montavimo tipas'] = dfv1['montavimo tipas'].apply(lambda x: str(x).replace('laikinas', 'įmontuojamas'))
    montipv= dfv1.groupby('montavimo tipas')['kaina'].mean().reset_index()
    
    dfp1=dfp
    dfp1 = dfp1.dropna(subset=['kaina'])
    dfp1['kaina'] = dfp1['kaina'].apply(lambda x: str(x).replace(' ', ''))
    dfp1['kaina']=dfp1['kaina'].astype(float)
    dfp1 = dfp1.dropna(subset=['montavimo tipas:'])
    montipp= dfp1.groupby('montavimo tipas:')['kaina'].mean().reset_index()
    
    montipp.rename(columns={'montavimo tipas:': 'montavimo tipas'}, inplace=True)
    montipp['pardavejas']='pigu.lt'
    montipv['pardavejas']='varle.lt'
    montipabu = pd.concat([montipp, montipv], axis=0, ignore_index=True)
    
    fig, ax  = plt.subplots(figsize=(10, 6))
    sns.barplot(data=montipabu, x='montavimo tipas', y='kaina', hue='pardavejas', palette='viridis')
    plt.title('Vidutinės kainos pagal montavimo tipą', fontsize=16)
    plt.xlabel('Montavimo Tipas', fontsize=14)
    plt.ylabel('Vidutinė kaina', fontsize=14)
    plt.legend(title='Pardavėjas', fontsize=12)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    dfv2 = dfv
    dfv2 = dfv2.dropna(subset=['tipas'])
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('fridge without freezer', 'šaldytuvas be šaldiklio'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('be kameros', 'šaldytuvas be šaldiklio'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('dviduriai', 'dviduris šaldytuvas'))

    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: 'mini šaldytuvas' if 'mini' in str(x) else x)
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('su kamera viršuje', 'šaldytuvas su šaldikliu viršuje'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('fridge with top freezer', 'šaldytuvas su šaldikliu viršuje'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('vitrina', 'vitrininis šaldytuvas'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('su kamera apačioje', 'šaldytuvas su šaldikliu apačioje'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('šaldytuvas su apatiniu šaldikliu', 'šaldytuvas su šaldikliu apačioje'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('šaldytuvas be šaldiklio', 'šaldytuvas be šaldiklio'))
    dfv2['tipas'] = dfv2['tipas'].apply(lambda x: str(x).replace('dviduris šaldytuvas', 'dviduris šaldytuvas'))

    dfv2 = dfv2[dfv2['tipas'].isin(['mini šaldytuvas','dviduris šaldytuvas', 'vitrininis šaldytuvas','šaldytuvas be šaldiklio', 'šaldytuvas su šaldikliu viršuje', 'šaldytuvas su šaldikliu apačioje', ])]

    tipasv= dfv2.groupby('tipas')['kaina'].mean().reset_index().sort_values('kaina')
    tipasv['pardavejas']='varle.lt'
    
    dfp2 = dfp
    dfp2 = dfp2.dropna(subset=['šaldytuvo tipas:'])
    dfp2 = dfp2[dfp2['šaldytuvo tipas:'].isin(['mini šaldytuvas','dviduris šaldytuvas', 'vitrininis šaldytuvas','šaldytuvas be šaldiklio', 'šaldytuvas su šaldikliu viršuje', 'šaldytuvas su šaldikliu apačioje', ])]

    tipasp= dfp2.groupby('šaldytuvo tipas:')['kaina'].mean().reset_index().sort_values('kaina')
    tipasp['pardavejas']= 'pigu.lt'
    tipasp.rename(columns={'šaldytuvo tipas:': 'tipas'}, inplace=True)
    
    tipasabu = pd.concat([tipasp, tipasv], axis=0, ignore_index=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=tipasabu, x='tipas', y='kaina', hue='pardavejas', palette='viridis')
    plt.title('Vidutinės kainos pagal tipą', fontsize=16)
    plt.xlabel('Tipas', fontsize=14)
    plt.ylabel('Vidutinė kaina', fontsize=14)
    plt.legend(title='Pardavėjas', fontsize=12)
    plt.xticks(rotation=15)
    plt.tight_layout()
    st.pyplot(fig)
    
    dfv3=dfv
    dfv3 = dfv3.dropna(subset=['gamintojas'])
    value_counts =list(dfv3['gamintojas'].value_counts().head(14).keys())
    dfv3 = dfv3[dfv3['gamintojas'].isin(value_counts)]
    dfv3=dfv3.sort_values('gamintojas')

    dfp3=dfp
    dfp3 = dfp3.dropna(subset=['prekės ženklas:'])
    value_counts =list(dfp3['prekės ženklas:'].value_counts().head(14).keys())
    dfp3 = dfp3[dfp3['prekės ženklas:'].isin(value_counts)]
    dfp3=dfp3.sort_values('prekės ženklas:')

    fig, (axis1, axis2) = plt.subplots(1,2, figsize=(10.5, 4.5))
    sns.boxplot(data=dfv3, y='gamintojas', x='kaina', showmeans=True, showfliers=False, ax=axis1)
    sns.boxplot(data=dfp3, y='prekės ženklas:', x='kaina', showmeans=True, showfliers=False, ax=axis2)
    axis1.set_title('varle.lt')
    axis2.set_title('pigu.lt')
    fig.tight_layout()
    st.pyplot(fig)
    
    dfp4=dfp
    dfp4 = dfp4.dropna(subset=['spalva:'])

    spalvukiek = dfp4['spalva:'].value_counts()
    spalvukiek = spalvukiek[spalvukiek > 100].index
    gamintojukiek = dfp4['prekės ženklas:'].value_counts()
    gamintojukiek = gamintojukiek[gamintojukiek >40].index

    dfp4 = dfp4[dfp4['prekės ženklas:'].isin(gamintojukiek) & dfp4['spalva:'].isin(spalvukiek)]
    dfp4=dfp4.groupby(['prekės ženklas:', 'spalva:'])['kaina'].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=dfp4, x='prekės ženklas:', y='kaina', hue='spalva:')
    plt.title('Vidutinė šaldytuvų kaina pagal gamintoją ir spalvą (pigu.lt)')
    plt.ylabel('Kaina')
    plt.xlabel('Gamintojas')
    plt.xticks(rotation=15)
    st.pyplot(fig)
    
    dfv5=dfv[['kaina', 'energijos klasė']]
    dfv5 = dfv5.dropna(subset=['energijos klasė'])
    dfv5['energijos klasė'] = dfv5['energijos klasė'].apply(lambda x: str(x).replace('+', ''))
    dfv5=dfv5.groupby(['energijos klasė'])['kaina'].mean().reset_index()
    dfv5['pardavejas']='varle.lt'
    dfp5=dfp[['kaina', 'energijos klasė:']]
    dfp5 = dfp5.dropna(subset=['energijos klasė:'])
    dfp5.rename(columns={'energijos klasė:': 'energijos klasė'}, inplace=True)
    dfp5=dfp5.groupby(['energijos klasė'])['kaina'].mean().reset_index()
    dfp5['pardavejas']='pigu.lt'
    dfvp5 = pd.concat([dfv5, dfp5], axis=0, ignore_index=True)

    fig, ax = plt.subplots()
    sns.lineplot(data=dfvp5, x='energijos klasė', y='kaina', hue='pardavejas')
    plt.title('Vidutinė šaldytuvų kaina pagal energetinę klasę')
    plt.ylabel('Kaina')
    plt.xlabel('Energijos klasė')
    plt.xticks(rotation=0)
    st.pyplot(fig)
    
    dfv6=dfv[['kaina', 'talpa (l)']]
    dfp6=dfp[['kaina', 'bendra talpa:']]
    dfp6.rename(columns={'bendra talpa:': 'talpa (l)'}, inplace=True)
    dfv6 = dfv6.dropna(subset=['talpa (l)'])
    dfv6['talpa (l)']=dfv6['talpa (l)'].astype(float)
    dfp6 = dfp6.dropna(subset=['talpa (l)'])
    dfp6['talpa (l)']=dfp6['talpa (l)'].apply(lambda x: x.replace(' ','').replace('l', ''))
    dfp6['talpa (l)']=dfp6['talpa (l)'].astype(float)
    dfvp6= pd.concat([dfv6, dfp6], axis=0, ignore_index=True)

    fig, ax = plt.subplots()
    sns.regplot(data=dfvp6,x='talpa (l)', y='kaina', order=2, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
    ax.set_xlabel('talpa (l)')
    ax.set_ylabel('Kaina')
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 3000)
    plt.title('Šaldytuvų kainų priklausomybė nuo talpos (varle.lt + pigu.lt)')
    st.pyplot(fig)
    
    dfp7 = dfp[['kaina', 'maksimalus triukšmo lygis:']]
    dfp7 = dfp7.dropna(subset=['maksimalus triukšmo lygis:'])
    dfp7['maksimalus triukšmo lygis:']=dfp7['maksimalus triukšmo lygis:'].apply(lambda x: x.replace(' ','').replace('db', '').replace('-',''))
    dfp7['maksimalus triukšmo lygis:'] = dfp7['maksimalus triukšmo lygis:'].replace([' ', '-', ''], None)
    dfp7 = dfp7.dropna(subset=['maksimalus triukšmo lygis:'])
    dfp7['maksimalus triukšmo lygis:']=dfp7['maksimalus triukšmo lygis:'].astype(float)

    fig, ax = plt.subplots()
    sns.regplot(data=dfp7,x='maksimalus triukšmo lygis:', y='kaina', order=2, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
    ax.set_xlabel('maksimalus triukšmo lygis (db)')
    ax.set_ylabel('Kaina')
    ax.set_xlim(30, 51)
    ax.set_ylim(0, 3000)
    plt.title('Šaldytuvų kainų priklausomybė nuo triukšmo (pigu.lt)')
    st.pyplot(fig)
    
    
if selected_option == 'Dronai':
    DB = sqlite3.connect('varledronai.db')
    C = DB.cursor()
    sql="""SELECT * FROM dronai;"""
    dfv = pd.read_sql_query(sql, con=DB)
    dfv['kaina']=dfv['kaina'].astype(float)
    DB = sqlite3.connect('pigudronai.db')
    C = DB.cursor()
    sql="""SELECT * FROM dronai;"""
    dfp = pd.read_sql_query(sql, con=DB)
    dfp = dfp.dropna(subset=['kaina'])
    dfp['kaina'] = dfp['kaina'].apply(lambda x: str(x).replace(' ', ''))
    dfp['kaina']=dfp['kaina'].astype(float)
    dfv1 = dfv[['kaina', 'gamintojas']]
    dfv1['pardavejas'] = 'varle.lt'
    dfp1 = dfp[['kaina', 'prekės ženklas:']]
    dfp1['pardavejas'] = 'pigu.lt'
    dfp1.rename(columns={'prekės ženklas:': 'gamintojas'}, inplace=True)

    spalvukiek = dfv1['gamintojas'].value_counts()
    spalvukiek = spalvukiek[spalvukiek > 3].index
    dfv1 = dfv1[dfv1['gamintojas'].isin(spalvukiek)]

    spalvukiek = dfp1['gamintojas'].value_counts()
    spalvukiek = spalvukiek[spalvukiek > 3].index
    dfp1 = dfp1[dfp1['gamintojas'].isin(spalvukiek)]

    dfpv1= pd.concat([dfv1, dfp1], axis=0, ignore_index=True)

    fig, (axis1, axis2) = plt.subplots(1,2, figsize=(10.5, 4.5))
    sns.boxplot(data=dfv1, y='gamintojas', x='kaina', showmeans=True, showfliers=False, ax=axis1)
    sns.boxplot(data=dfp1, y='gamintojas', x='kaina', showmeans=True, showfliers=False, ax=axis2)
    axis1.set_title('varle.lt')
    axis2.set_title('pigu.lt')
    fig.tight_layout()
    axis1.set_xlim(0, 10000)
    st.pyplot(fig)
    
    dfv2=dfv[['kaina', 'didžiausias skrydžio laikas']]
    dfp2=dfp[['kaina', 'skraidymo laikas:']]
    dfv2.rename(columns={'didžiausias skrydžio laikas': 'skraidymo laikas:'}, inplace=True)

    dfpv2= pd.concat([dfv2, dfp2], axis=0, ignore_index=True)

    dfpv2 = dfpv2.dropna(subset=['skraidymo laikas:'])
    dfpv2['skraidymo laikas:'] = dfpv2['skraidymo laikas:'].str.replace(
        r'\b(minutes|min\.|minučių|minutė|)\b', '', regex=True
    ).str.strip()

    dfpv2['skraidymo laikas:'] = (
        dfpv2['skraidymo laikas:']
        .str.strip()
        .str.replace(r'\s*min\*?', '', regex=True) 
    )
    dfpv2['skraidymo laikas:'] = dfpv2['skraidymo laikas:'].replace(['', '-', '.', '-.'], None)
    dfpv2 = dfpv2.dropna(subset=['skraidymo laikas:'])
    dfpv2['skraidymo laikas:']=dfpv2['skraidymo laikas:'].astype(float)

    fig, ax = plt.subplots()
    sns.regplot(data=dfpv2,x='skraidymo laikas:', y='kaina', order=1, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
    ax.set_xlabel('skraidymo laikas (min.)')
    ax.set_ylabel('Kaina')
    # ax.set_xlim(30, 55)
    ax.set_ylim(0, 3000)
    plt.title('Dronų kainų priklausomybė nuo skraidymo laiko (pigu.lt + varle.lt)')
    st.pyplot(fig)
    
    dfp3 = dfp[['kaina', 'veikimo atstumas:']]
    dfp3 = dfp3.dropna(subset=['veikimo atstumas:'])
    dfp3['veikimo atstumas:']=dfp3['veikimo atstumas:'].apply(lambda x: x.replace(' ','').replace('m', '').replace('-',''))
    dfp3['veikimo atstumas:'] = dfp3['veikimo atstumas:'].replace([' ', '-', ''], None)
    dfp3 = dfp3.dropna(subset=['veikimo atstumas:'])
    dfp3['veikimo atstumas:']=dfp3['veikimo atstumas:'].astype(float)

    fig, ax = plt.subplots()
    sns.regplot(data=dfp3,x='veikimo atstumas:', y='kaina', order=1, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
    ax.set_xlabel('skraidymo nuotolis (metrais)')
    ax.set_ylabel('Kaina')
    # ax.set_xlim(30, 55)
    ax.set_ylim(0, 3000)
    plt.title('Dronų kainų priklausomybė nuo skraidymo nuotolio (pigu.lt)')
    st.pyplot(fig)
    
    dfv3 = dfv[['kaina', 'svoris (su baterija, g)']]
    dfp3=dfp[['kaina', 'svoris:']]
    dfv3.rename(columns={'svoris (su baterija, g)': 'svoris:'}, inplace=True)
    dfpv3= pd.concat([dfv3, dfp3], axis=0, ignore_index=True)

    dfpv3['svoris:']=dfpv3['svoris:'].apply(lambda x: str(x).replace(' ','').replace('g', '').replace('-',''))
    dfpv3['svoris:'] = dfpv3['svoris:'].replace([' ', '-', '','None'], None)
    dfpv3 = dfpv3.dropna(subset=['svoris:'])
    dfpv3['svoris:'] = pd.to_numeric(dfpv3['svoris:'], errors='coerce')

    fig, ax = plt.subplots()
    sns.regplot(data=dfpv3,x='svoris:', y='kaina', order=6, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
    ax.set_xlabel('svoris gramais')
    ax.set_ylabel('Kaina')
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 4000)
    plt.title('Dronų kainų priklausomybė nuo svorio (pigu.lt)')
    st.pyplot(fig)
    
    dfp4=dfp[['kaina', 'gps:']]
    dfp4['gps:']=dfp4['gps:'].str.replace('nenurodyta', 'nėra')

    fig, ax = plt.subplots()
    sns.boxplot(data=dfp4, y='kaina', x='gps:', showmeans=True, showfliers=False, ax=ax)
    ax.set_title('ar yra GPS. pigu.lt')
    fig.tight_layout()
    # ax.set_xlim(0, 10000)
    st.pyplot(fig)
    
    dfv5=dfv[['kaina', 'didžiausias skrydžio laikas', 'perdavimo atstumas (lauke ir be kliūčių)', 'svoris (su baterija, g)', 'gps', 'stabilizavimas']]
    dfp5=dfp[['kaina', 'skraidymo laikas:', 'veikimo atstumas:', 'svoris:', 'gps:', 'skrydžio stabilizacija:']]
    dfv5.rename(columns={'didžiausias skrydžio laikas': 'skraidymo laikas:'}, inplace=True)
    dfv5.rename(columns={'perdavimo atstumas (lauke ir be kliūčių)': 'veikimo atstumas:'}, inplace=True)
    dfv5.rename(columns={'svoris (su baterija, g)': 'svoris:'}, inplace=True)
    dfv5.rename(columns={'gps': 'gps:'}, inplace=True)
    dfp5.rename(columns={'skrydžio stabilizacija:': 'stabilizavimas'}, inplace=True)

    dfpv5= pd.concat([dfv5, dfp5], axis=0, ignore_index=True)

    dfpv5['skraidymo laikas:']=dfpv5['skraidymo laikas:'].apply(lambda x: str(x).replace(' ','').replace('minutes', '').replace('minutė',''))
    dfpv5['skraidymo laikas:']=dfpv5['skraidymo laikas:'].apply(lambda x: str(x).replace('minučių','').replace('min.', '').replace('-min.','').replace('-', ''))
    dfpv5['skraidymo laikas:'] = dfpv5['skraidymo laikas:'].replace(['', ' ', 'None'], None)
    # dfpv5['skraidymo laikas:'] = dfpv5['skraidymo laikas:'].apply(lambda x: float(x))
    dfpv5['veikimo atstumas:'] = dfpv5['veikimo atstumas:'].apply(lambda x: str(x).split(',')[0])
    dfpv5['veikimo atstumas:']=dfpv5['veikimo atstumas:'].apply(lambda x: str(x).replace('ce:','').replace('eb:', '').replace('m','').replace(' ', ''))
    dfpv5['veikimo atstumas:']=dfpv5['veikimo atstumas:'].apply(lambda x: str(x).replace('fcc:','').replace('-', ''))
    dfpv5['veikimo atstumas:'] = dfpv5['veikimo atstumas:'].replace(['', ' ', 'None'], None)
    # dfpv5['skraidymo laikas:'] = dfpv5['skraidymo laikas:'].apply(lambda x: float(x))
    # dfp3 = dfp3.dropna(subset=['veikimo atstumas:'])
    dfpv5['svoris:']=dfpv5['svoris:'].apply(lambda x: str(x).replace('g','').replace(' ', '').replace('-', ''))
    dfpv5['svoris:'] = dfpv5['svoris:'].apply(lambda x: float(x)*1000 if '.' in str(x) else x)
    dfpv5['svoris:'] = dfpv5['svoris:'].replace(['', ' ', 'None'], None)

    dfpv5['gps:']=dfpv5['gps:'].apply(lambda x: str(x).replace('taip','yra').replace('nenurodyta', 'nėra').replace('-', ''))
    dfpv5['gps:'] = dfpv5['gps:'].replace(['', ' ', 'None'], None)

    dfpv5['stabilizavimas']=dfpv5['stabilizavimas'].apply(lambda x: str(x).replace('3 ašių (3-axis)','yra').replace('nenurodyta', 'nėra').replace('vienos ašies', ''))
    dfpv5['stabilizavimas'] = dfpv5['stabilizavimas'].replace(['', ' ', 'None'], None)
    
    dfpv5['kaina100']=dfpv5['kaina'].apply(lambda x: np.ceil(x/100)*100)
    dfpv5['kaina100']=dfpv5['kaina100'].apply(lambda x: x if x<700 else 700 )
    dfpv5['kaina100']=dfpv5['kaina100'].apply(lambda x: 400 if x==300 else x )
    dfpv5['kaina100']=dfpv5['kaina100'].apply(lambda x: 600 if x==500 else x )
    
    def skraidymolaikas(df, eur):
        skraidymo_laikas= df
        skraidymo_laikas = skraidymo_laikas[skraidymo_laikas['kaina100'] == eur][['skraidymo laikas:']]
        skraidymo_laikas = skraidymo_laikas.dropna(subset=['skraidymo laikas:'])
        skraidymo_laikas['skraidymo laikas:'] = skraidymo_laikas['skraidymo laikas:'].astype(float)
        skraidymo_laikas= round(skraidymo_laikas['skraidymo laikas:'].mean())
        return skraidymo_laikas
    def veikimoatstumas(df, eur):
        veikimo_atstumas = df
        veikimo_atstumas = veikimo_atstumas[veikimo_atstumas['kaina100'] == eur][['veikimo atstumas:']]
        veikimo_atstumas = veikimo_atstumas.dropna(subset=['veikimo atstumas:'])
        veikimo_atstumas['veikimo atstumas:'] = veikimo_atstumas['veikimo atstumas:'].astype(float)
        veikimo_atstumas= round(veikimo_atstumas['veikimo atstumas:'].mean())
        return veikimo_atstumas
    def svoris(df, eur):
        svoris = df
        svoris = svoris[svoris['kaina100'] == eur][['svoris:']]
        svoris = svoris.dropna(subset=['svoris:'])
        svoris['svoris:'] = svoris['svoris:'].astype(float)
        svoris= round(svoris['svoris:'].mean()) 
        return svoris
    def gps(df, eur):
        gps = df
        gps = gps[gps['kaina100'] == eur][['gps:']]
        gpsyra = len(gps[gps['gps:'] == 'yra'])
        gpsnera = len(gps[gps['gps:'] == 'nėra'])
        gps = round(gpsyra/(gpsyra+ gpsnera)*100)
        return gps
    def stabilizavimas(df, eur):
        stabilizavimas = df
        stabilizavimas = stabilizavimas[stabilizavimas['kaina100'] == eur][['stabilizavimas']]
        stabilizavimasyra = len(stabilizavimas[stabilizavimas['stabilizavimas'] == 'yra'])
        stabilizavimasnera = len(stabilizavimas[stabilizavimas['stabilizavimas'] == 'nėra'])
        stabilizavimas = round(stabilizavimasyra/(stabilizavimasyra+ stabilizavimasnera)*100)
        return stabilizavimas
    
    # for i in [100, 200, 400, 600, 700]:
    #     st.write(f'tikėtinas dronas, kurio vertė iki  {i}')
    #     st.write('skraidymo laikas:', skraidymolaikas(dfpv5, i))
    #     st.write('veikimo atstumas:', veikimoatstumas(dfpv5, i))
    #     st.write('svoris:', svoris(dfpv5, i))
    #     st.write('gps tikimybė:', gps(dfpv5, i), '%')
    #     st.write('stabilizatoriaus tikimybė:', stabilizavimas(dfpv5, i), '%')
        
    st.write(f'tikėtinas dronas, kurio vertė 0-100,    101-200,    201-400,    401-600,    600++')
    st.write('skraidymo laikas:', skraidymolaikas(dfpv5, 100), skraidymolaikas(dfpv5, 200), skraidymolaikas(dfpv5, 400), skraidymolaikas(dfpv5, 600), skraidymolaikas(dfpv5, 700))
    st.write('veikimo atstumas:', veikimoatstumas(dfpv5, 100), veikimoatstumas(dfpv5, 200), veikimoatstumas(dfpv5, 400), veikimoatstumas(dfpv5, 600), veikimoatstumas(dfpv5, 700))
    st.write('svoris:', svoris(dfpv5, 100), svoris(dfpv5, 200), svoris(dfpv5, 400), svoris(dfpv5, 600), svoris(dfpv5, 700))
    st.write('gps tikimybė:', gps(dfpv5, 100), '%', gps(dfpv5, 200), '%', gps(dfpv5, 400), '%', gps(dfpv5, 600), '%', gps(dfpv5, 700), '%')
    st.write('stabilizatoriaus tikimybė:', stabilizavimas(dfpv5, 100), '%', stabilizavimas(dfpv5, 200), '%', stabilizavimas(dfpv5, 400), '%', stabilizavimas(dfpv5, 600), '%', stabilizavimas(dfpv5, 700), '%')
    
    
if selected_option == 'Planšetiniai kompiuteriai':
    DB = sqlite3.connect('varletablets.db')
    C = DB.cursor()
    sql="""SELECT * FROM tablets;"""
    dfv = pd.read_sql_query(sql, con=DB)
    dfv['kaina']=dfv['kaina'].astype(float)

    DB = sqlite3.connect('pigutablets.db')
    C = DB.cursor()
    sql="""SELECT * FROM tablets;"""
    dfp = pd.read_sql_query(sql, con=DB)
    dfp = dfp.dropna(subset=['kaina'])
    dfp['kaina'] = dfp['kaina'].apply(lambda x: str(x).replace(' ', ''))
    dfp['kaina']=dfp['kaina'].astype(float)
    dfv1 = dfv[['kaina', 'gamintojas']]
    dfv1['pardavejas'] = 'varle.lt'
    dfp1 = dfp[['kaina', 'prekės ženklas:']]
    dfp1['pardavejas'] = 'pigu.lt'
    dfp1.rename(columns={'prekės ženklas:': 'gamintojas'}, inplace=True)
    dfpv1= pd.concat([dfv1, dfp1], axis=0, ignore_index=True)
    spalvukiek = dfv1['gamintojas'].value_counts()
    spalvukiek = spalvukiek[spalvukiek > 20].index
    dfv1 = dfv1[dfv1['gamintojas'].isin(spalvukiek)]

    spalvukiek = dfp1['gamintojas'].value_counts()
    spalvukiek = spalvukiek[spalvukiek > 20].index
    dfp1 = dfp1[dfp1['gamintojas'].isin(spalvukiek)]
    
    fig, (axis1, axis2) = plt.subplots(1,2)
    sns.boxplot(data=dfv1, y='gamintojas', x='kaina', showmeans=True, showfliers=False, ax=axis1)
    sns.boxplot(data=dfp1, y='gamintojas', x='kaina', showmeans=True, showfliers=False, ax=axis2)
    axis1.set_title('varle.lt')
    axis2.set_title('pigu.lt')
    fig.tight_layout()
    axis1.set_xlim(0, 4000)
    axis2.set_xlim(0, 2000)
    st.pyplot(fig)
    
    kainoshead5= dfpv1.groupby('gamintojas')['kaina'].mean().reset_index().sort_values('kaina', ascending=False).head(5)
    kainostail5= dfpv1.groupby('gamintojas')['kaina'].mean().reset_index().sort_values('kaina', ascending=False).tail(5)
    gamintojas_kaina = dfpv1.groupby('gamintojas')['kaina'].mean().reset_index().sort_values('kaina', ascending=False)
    middle_index = len(gamintojas_kaina) // 2
    if len(gamintojas_kaina) % 2 == 0:
        middle_5_gamintojas = gamintojas_kaina.iloc[middle_index - 3: middle_index + 2]
    else:
        middle_5_gamintojas = gamintojas_kaina.iloc[middle_index - 2: middle_index + 3]
        
    st.write(f'5 brangiausi gamintojai: {list(kainoshead5['gamintojas'])}')
    st.write(f'5 pigiausi gamintojai: {list(kainostail5['gamintojas'])}')
    st.write(f'5 vidutinės kainos gamintojai: {list(middle_5_gamintojas['gamintojas'])}')
    
    dfp2=dfp[['kaina', 'ekrano įstrižainė:', 'operatyvinė atmintis (ram):', 'vidinė atmintis:']]
    dfp2['ekrano įstrižainė:']=dfp2['ekrano įstrižainė:'].apply(lambda x: str(x).replace('"',' ').split(' ')[0])
    dfp2['ekrano įstrižainė:']=dfp2['ekrano įstrižainė:'].apply(lambda x: str(x).replace("''",' ').replace('”', ''))
    dfp2['ekrano įstrižainė:'] = dfp2['ekrano įstrižainė:'].replace(['', 'kiti', 'None', 'nenurodyta', '27,9cm'], None)
    # dfp2 = dfp2.dropna(subset=['ekrano įstrižainė:'])
    dfp2['ekrano įstrižainė:']=dfp2['ekrano įstrižainė:'].astype(float)
    dfp2['operatyvinė atmintis (ram):']=dfp2['operatyvinė atmintis (ram):'].apply(lambda x: str(x).replace("-",' ').replace('mb', '').replace(' ',''))
    dfp2['operatyvinė atmintis (ram):']=dfp2['operatyvinė atmintis (ram):'].replace(['', 'None'], None)
    dfp2['operatyvinė atmintis (ram):']=dfp2['operatyvinė atmintis (ram):'].astype(float)
    dfp2['operatyvinė atmintis (ram):']=dfp2['operatyvinė atmintis (ram):'].apply(lambda x: float(x)*1000 if float(x)<100 else x)
    dfp2['vidinė atmintis:']=dfp2['vidinė atmintis:'].apply(lambda x: str(x).split(' ')[0])
    dfp2['vidinė atmintis:']=dfp2['vidinė atmintis:'].apply(lambda x: str(x).replace("gb",'').replace('None', '').replace('nenurodyta',''))
    dfp2['vidinė atmintis:']=dfp2['vidinė atmintis:'].replace(['', 'None'], None)
    dfp2['vidinė atmintis:']=dfp2['vidinė atmintis:'].astype(float)
    dfp2['vidinė atmintis:']=dfp2['vidinė atmintis:'].apply(lambda x: float(x)*1000 if float(x)<3 else x)
    dfv2=dfv[['kaina', 'ekrano įstrižainė', 'atmintis (ram) (gb)', 'vidinė atmintis (gb)']]
    dfv2['ekrano įstrižainė']=dfv2['ekrano įstrižainė'].apply(lambda x: str(x).replace('"',' ').replace("''", " ").split(' ')[0])
    dfv2['ekrano įstrižainė'] = dfv2['ekrano įstrižainė'].apply(lambda x: x.replace(',', '.'))
    dfv2['ekrano įstrižainė'] = dfv2['ekrano įstrižainė'].replace(['', 'None'], None)
    # dfv2 = dfv2.dropna(subset=['ekrano įstrižainė'])
    dfv2['ekrano įstrižainė'] = dfv2['ekrano įstrižainė'].astype(float)
    dfv2['atmintis (ram) (gb)']=dfv2['atmintis (ram) (gb)'].apply(lambda x: str(x).replace(' ', ''))
    dfv2['atmintis (ram) (gb)']=dfv2['atmintis (ram) (gb)'].replace(['', 'None'], None)
    dfv2['atmintis (ram) (gb)']=dfv2['atmintis (ram) (gb)'].astype(float)
    dfv2['atmintis (ram) (gb)']=dfv2['atmintis (ram) (gb)'].apply(lambda x: float(x)*1000 if float(x)<100 else x)
    dfv2['vidinė atmintis (gb)']=dfv2['vidinė atmintis (gb)'].apply(lambda x: str(x).replace(' ', ''))
    dfv2['vidinė atmintis (gb)']=dfv2['vidinė atmintis (gb)'].replace(['', 'None'], None)
    dfv2['vidinė atmintis (gb)']=dfv2['vidinė atmintis (gb)'].astype(float)
    
    # Streamlit app
    st.title("Pairplot pigu.lt")
    # Generate the pairplot
    def generate_pairplot(data):
        pairplot = sns.pairplot(data)
        return pairplot
    # Create pairplot and display in Streamlit
    with st.spinner("Generating Pairplot..."):
        pairplot = generate_pairplot(dfp2)
    # Save and display the plot in Streamlit
    st.pyplot(pairplot)

    # Streamlit app
    st.title("Pairplot varle.lt")
    # Generate the pairplot
    def generate_pairplot(data):
        pairplot = sns.pairplot(data)
        return pairplot
    # Create pairplot and display in Streamlit
    with st.spinner("Generating Pairplot..."):
        pairplot = generate_pairplot(dfv2)
    # Save and display the plot in Streamlit
    st.pyplot(pairplot)
    
    
    dt=dfp2[['kaina', 'operatyvinė atmintis (ram):', 'ekrano įstrižainė:','vidinė atmintis:']].corr(numeric_only=True)
    st.title("Heatmap pigu.lt")
    # Generate the heatmap
    def generate_heatmap(data):
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
        sns.heatmap(data, annot=True, annot_kws={'fontsize': 12}, fmt=".0f", ax=ax, cmap="coolwarm")
        ax.set_title("Heatmap of Data", fontsize=16)
        return fig

    # Create and display heatmap in Streamlit
    with st.spinner("Generating Heatmap..."):
        heatmap_fig = generate_heatmap(dt)

        st.pyplot(heatmap_fig)
    
    
    
    
    dt=dfv2[['kaina', 'ekrano įstrižainė', 'atmintis (ram) (gb)','vidinė atmintis (gb)']].corr(numeric_only=True)
    st.title("Heatmap varle.lt")
    # Generate the heatmap
    def generate_heatmap(data):
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
        sns.heatmap(data, annot=True, annot_kws={'fontsize': 24}, fmt=".0f", ax=ax)
        plt.title("Heatmap of Data")
        return fig
    # Create and display heatmap in Streamlit
    with st.spinner("Generating Heatmap..."):
        heatmap_fig = generate_heatmap(dt)
    st.pyplot(heatmap_fig)
    
    
    
    
if selected_option == 'Televizoriai':
    st.write('tirlim pirlim')
    
if selected_option == 'Dviračiai':
    st.write('Pirlim tirlim')