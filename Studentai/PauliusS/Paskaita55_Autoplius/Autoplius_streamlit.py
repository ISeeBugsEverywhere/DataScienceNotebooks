import numpy as np                  # "numpy" yra biblioteka darbui su didelėmis, daugiamatėmis masyvų ir matricų kolekcijomis bei matematinėmis funkcijomis
import pandas as pd                 # "pandas" suteikia struktūras duomenims ir įrankius jų analizei, pvz., DataFrame
import matplotlib.pyplot as plt     # "matplotlib.pyplot" yra vizualizacijos biblioteka, leidžianti piešti įvairius grafikus
import warnings                     # "warnings" leidžia valdyti įspėjimus: juos ignoruoti, spausdinti, ar klaidinti
import requests                     # "requests" leidžia siųsti HTTP užklausas naudojant Python
from datetime import datetime       # "datetime" modulis suteikia funkcijas darbui su data ir laiku
from bs4 import BeautifulSoup       # "BeautifulSoup" padeda atlikti internetinių puslapių šaltinio kodo (HTML, XML) analizę ir duomenų surinkimą
import time                         # "time" modulis suteikia funkcijas, susijusias su laiku, pvz., laiko gaišimą ar laiko matavimą
import sqlite3                      # "sqlite3" leidžia dirbti su SQLite duomenų bazėmis, atliekant duomenų saugojimo, atnaujinimo ir gavimo operacijas
from numpy.polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')   # Nustato, kad visi įspėjimai būtų ignoruojami
from selenium import webdriver                          # "selenium.webdriver" leidžia automatizuoti veiksmus interneto naršyklėje
from selenium.webdriver.chrome.options import Options 


############ ############ ############ ############ ############ ############ ############ ############ ############


# 1. Susirenkame lenteles 
def issitraukiame_duomenis(x):

    # Atidarome duomenų bazę
    SDB = sqlite3.connect(x)
    
    # Pirma lentele
    sql_url = "SELECT * FROM TUrl;"
    df1 = pd.read_sql_query(sql_url, con=SDB)
    df1['kaina'] = [x.split(';')[-1] for x in df1['params']]  # Išskaidome kainą
    df1['kaina_int'] = df1['kaina'].str.replace(' €', '').str.replace(" ", "").str.split('\n').str[-1].astype(int)

    # Antra lentele
    sql_autos = "SELECT * FROM TAutos;"
    df2 = pd.read_sql_query(sql_autos, con=SDB)
    # Išimame gamintojus 'Kita'
    df2 = df2.loc[df2['gamintojas'] != '-Kita-']
    # Paverčiame Metus į integerius
    df2 = df2[df2['Pirma registracija'].notna()]
    df2['Pirma registracija'] = df2['Pirma registracija'].astype(str)
    df2['Pirma registracija'] = df2['Pirma registracija'].str[:4].astype(int)
    df2 = df2[df2['Pirma registracija'] > 1980]
    # Paverčiame ridas į integerius
    df2 = df2[df2['Rida'].notna()]
    df2['Rida'] = df2['Rida'].str.replace(' km', '').str.replace(" ", "").astype(int)
    df2 = df2[df2['Rida'] < 500000]
    df2 = df2[df2['Rida'] > 1]
    df2['Rida'] = np.ceil(df2['Rida'] / 5000) * 5000

    # Uždarome duomenų bazę
    SDB.close()
    
    # Pakeičiame stulpelių pavadinimus
    df2 = df2.rename(columns={'Kuro tipas': 'kuras', 'Pirma registracija': 'metai', 'Kėbulo tipas': 'kebulas'})
    
    # Sujungimas pagal 'id'
    df2 = pd.merge(df1[['id', 'kaina_int']], df2, on='id', how='inner')

    # Atrenkame norimus stulpelius
    df3 = df2[['metai', 'kaina_int', 'gamintojas', 'Rida', 'kebulas', 'kuras']]

    return df3

x = 'C:\\Users\\Pauliussl\\OneDrive - REWE International AG\\Desktop\\Kodai5\\DataScienceNotebooks\\Studentai\\PauliusS\\Paskaita55_Autoplius\\WEBscr.db'
df3 = issitraukiame_duomenis(x)
df3.head()

