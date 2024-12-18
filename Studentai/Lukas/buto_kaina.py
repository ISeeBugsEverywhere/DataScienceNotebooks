import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
# import plotly.express as px
# import numpy.polynomial.polynomial as poly
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')


SDB = sqlite3.connect('aruodas.db')
C = SDB.cursor()
sql="""select *   from Aruodas;"""
df = pd.read_sql_query(sql, con=SDB)

SDB.close()

def plotas(x):
    # if 'm²' in x:
    if x is not None:
        return float(x.replace(' m²', '',).replace(',', '.'))
    else:
        return np.nan
    
df['plotas'] = df['Plotas:'].apply(plotas)

def amzius(x):
    return  2024 - int(x[:4])

df['amzius'] = df['Metai:'].apply(amzius)

aruodas = df[['miestas', 'rajonas', 'gatve', 'kaina', 'kv_kaina', 'Kambarių sk.:',
       'Aukštas:', 'Aukštų sk.:', 'Pastato tipas:', 'Šildymas:',
       'Įrengimas:','plotas', 'amzius']]
aruodas.dropna(inplace=True)

aruodas['Kambarių sk.:'] = aruodas['Kambarių sk.:'].apply(lambda x: int(x))
aruodas['Aukštas:'] = aruodas['Aukštas:'].apply(lambda x: int(x))
aruodas['Aukštų sk.:'] = aruodas['Aukštų sk.:'].apply(lambda x: int(x))

#  pasirinkimai
# # Extract unique values from the 'Category' column
# unique_categories = df['Category'].unique()
# # Display them in a selectbox in Streamlit
# selected_category = st.selectbox('Select a Category', unique_categories)

# uniq_miestas = aruodas['miestas'].unique()
# selected_mietas = st.selectbox('Pasirinkite miestą', uniq_miestas)

encoder = LabelEncoder()
aruodas['City_Encoded'] = encoder.fit_transform(aruodas['miestas'])
uniq_miestas = aruodas['miestas'].unique()
selected_miestas = st.selectbox('Pasirinkite miestą', uniq_miestas)
selected_miestas_index = encoder.transform([selected_miestas])[0]
st.write(f'You selected: {selected_miestas} (Encoded label: {selected_miestas_index})')

aruodas['rajonas_Encoded'] = encoder.fit_transform(aruodas['rajonas'])
uniq_rajonas = aruodas['rajonas'].unique()
selected_rajonas = st.selectbox('Pasirinkite rajoną', uniq_rajonas)
selected_rajonas_index = encoder.transform([selected_rajonas])[0]
st.write(f'You selected: {selected_rajonas} (Encoded label: {selected_rajonas_index})')

aruodas['gatve_Encoded'] = encoder.fit_transform(aruodas['gatve'])
uniq_gatve = aruodas['gatve'].unique()
selected_gatve = st.selectbox('Pasirinkite gatvę', uniq_gatve)
selected_gatve_index = encoder.transform([selected_gatve])[0]
st.write(f'You selected: {selected_gatve} (Encoded label: {selected_gatve_index})')

aruodas['tipas_Encoded'] = encoder.fit_transform(aruodas['Pastato tipas:'])
uniq_tipas = aruodas['Pastato tipas:'].unique()
selected_tipas = st.selectbox('Pasirinkite pastato tipą', uniq_tipas)
selected_tipas_index = encoder.transform([selected_tipas])[0]
st.write(f'You selected: {selected_tipas} (Encoded label: {selected_tipas_index})')

aruodas['sildymas_Encoded'] = encoder.fit_transform(aruodas['Šildymas:'])
uniq_sildymas = aruodas['Šildymas:'].unique()
selected_sildymas = st.selectbox('Pasirinkite šildymo tipą', uniq_sildymas)
selected_sildymas_index = encoder.transform([selected_sildymas])[0]
st.write(f'You selected: {selected_sildymas} (Encoded label: {selected_sildymas_index})')

aruodas['irengimas_Encoded'] = encoder.fit_transform(aruodas['Įrengimas:'])
uniq_irengimas = aruodas['Įrengimas:'].unique()
selected_irengimas = st.selectbox('Pasirinkite įrengimą', uniq_irengimas)
selected_irengimas_index = encoder.transform([selected_irengimas])[0]
st.write(f'You selected: {selected_irengimas} (Encoded label: {selected_irengimas_index})')

uniq_kamb = aruodas['Kambarių sk.:'].unique()
selected_kamb = st.selectbox('Pasirinkite kambarių skaičių', uniq_kamb)

uniq_aukstas = aruodas['Aukštas:'].unique()
selected_aukstas = st.selectbox('Pasirinkite buto aukštą', uniq_aukstas)

uniq_austu_sk = aruodas['Aukštų sk.:'].unique()
selected_austu_sk = st.selectbox('Pasirinkite kiek namas turi aukštų', uniq_austu_sk)





# vertinimui
# l = LabelEncoder().fit_transform(aruodas['miestas'])
# aruodas['miestas'] = l
# l = LabelEncoder().fit_transform(aruodas['rajonas'])
# aruodas['rajonas'] = l
# l = LabelEncoder().fit_transform(aruodas['gatve'])
# aruodas['gatve'] = l
# l = LabelEncoder().fit_transform(aruodas['Pastato tipas:'])
# aruodas['Pastato tipas:'] = l
# l = LabelEncoder().fit_transform(aruodas['Šildymas:'])
# aruodas['Šildymas:'] = l
# l = LabelEncoder().fit_transform(aruodas['Įrengimas:'])
# aruodas['Įrengimas:'] = l

X = aruodas.drop(columns=['kaina', 'kv_kaina','miestas','rajonas','gatve', 'Pastato tipas:','Šildymas:' ,'Įrengimas:'])
y = aruodas['kaina'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

fit = LinearRegression().fit(X_train, y_train)
predicted = fit.predict(X_test)

spejimai = pd.Series(data=predicted, name='Spejimai')
orig_rez = pd.Series(data=y_test, name='YTest')
res = pd.concat([orig_rez.reset_index(drop=True), spejimai], axis=1)
# res.head()
fit_score = fit.score(X_test, y_test) * 100.0
st.write(f'fit score: {fit_score}')

miestas = selected_miestas_index
rajonas = selected_rajonas_index
gatve = selected_gatve_index
Kambariu_sk = selected_kamb
aukstas = selected_aukstas
Aukstu_s = selected_austu_sk
Pastato_tipas = selected_tipas_index
sildymas = selected_sildymas_index
irengimas = selected_irengimas_index
area = 50           # pasidaryti pasirinkimus
amz = 1             # pasidaryti pasirinkimus


ats = fit.predict(np.reshape([miestas, rajonas, gatve, Kambariu_sk, aukstas, Aukstu_s, Pastato_tipas, sildymas, irengimas, area, amz], (1, -1)))
print(f'mpg: {float(ats):.2f}')