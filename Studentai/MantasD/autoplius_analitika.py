import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Funkcija, kuri gauna duomenis iš SQLite duomenų bazės
def query_to_dataframe(db_path, query):
    import sqlite3
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Nuskaitome duomenis iš duomenų bazės
db_path = 'web_scrap.db'
query = 'SELECT * FROM autopliuslt2;'
df = query_to_dataframe(db_path, query)

# Duomenų apdorojimas
dft = df.copy()
dft['Kaina'] = dft['Kaina'].apply(lambda x: float(x))
dft['Rida'] = dft['Rida'].apply(lambda x: x[:-3].replace(' ','') if x != None else x)
dft['Rida'] = dft['Rida'].apply(lambda x: float(x) if x != None and x != '' else x)
dft['Rida_group'] = dft['Rida'].apply(lambda x: np.ceil(x/50000)*50000)
dft['Amžius'] = dft['Pirma registracija'].apply(lambda x: (np.ceil((2024-int(x[:4]))/5))*5 if x != None else x)
dft['Amžius2'] = dft['Pirma registracija'].apply(lambda x: int(2024-int(x[:4])) if x != None else x)

def kw(x):
    if x != None:
        if 'kW' in x:
            return int((np.ceil(int(x.split('(')[1].replace('kW)',''))/20))*20)
        else:
            return None
    else:
        return None
    
def kw2(x):
    if x != None:
        if 'kW' in x:
            return int(x.split('(')[1].replace('kW)',''))
        else:
            return None
    else:
        return None

dft['Galingumas'] = dft['Variklis'].apply(kw)
dft['Galingumas2'] = dft['Variklis'].apply(kw2)
dft['Tik Miestas'] = dft['Miestas'].apply(lambda x: x.split(',')[0] if x!=None else None)
dft['TA'] = dft['Tech. apžiūra iki'].apply(lambda x: int(x[:4]) if x != None else None)
dft['Galioja_TA'] = dft['TA'].apply(lambda x: "Taip" if x>2024 else 'Ne')
dft['TA_m'] = dft['TA'].apply(lambda x: str(int(x)) if x>2024 else 'Negalioja')

st.title('Automobilių kainų analizė')

# Pasirinkimas grafiko iš sąrašo
options = [
    'Kainos priklausomybė nuo ridos',
    'Kainos priklausomybė nuo amžiaus',
    'Kainos priklausomybė nuo galingumo',
    'Kainos priklausomybė nuo kėbulo tipo',
    'Kainos priklausomybė nuo pavarų dėžės',
    'Kainos priklausomybė nuo miesto',
    'Kainos priklausomybė nuo pirmosios registracijos šalies',
    'Kainos priklausomybė nuo TA galiojimo',
    'Populiariausi automobilių markės'
]

# Vartotojas gali pasirinkti grafiką
selected_option = st.selectbox('Pasirinkite grafiką:', options)

# Funkcija grafiko rodymui pagal pasirinkimą
def show_chart(selected_option):
    fig, axes = plt.subplots(figsize=(16, 8))

    if selected_option == 'Kainos priklausomybė nuo ridos':
        dfx = dft.groupby(['Rida_group'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Rida_group', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo ridos')
        axes.set(xlabel='Rida', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo amžiaus':
        dfx = dft.groupby(['Amžius'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Amžius', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo amžiaus')
        axes.set(xlabel='Amžius', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo galingumo':
        dfx = dft[dft['Galingumas'].notna()].groupby(['Galingumas'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Galingumas', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo galingumo')
        axes.set(xlabel='Galingumas (kW)', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo kėbulo tipo':
        dfx = dft.groupby(['Kėbulo tipas'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Kėbulo tipas', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo kėbulo tipo')
        axes.set(xlabel='Kėbulo tipas', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo pavarų dėžės':
        dfx = dft.groupby(['Pavarų dėžė'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Pavarų dėžė', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo pavarų dėžės')
        axes.set(xlabel='Pavarų dėžė', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo miesto':
        dfx = dft.groupby(['Tik Miestas'])['Kaina'].mean().reset_index().sort_values(by='Kaina', ascending=True)
        sns.barplot(data=dfx, x='Tik Miestas', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo miesto')
        axes.set(xlabel='Miestas', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo pirmosios registracijos šalies':
        dfx = dft.groupby(['Pirmosios registracijos šalis'])['Kaina'].mean().reset_index().sort_values(by='Kaina', ascending=True)
        sns.barplot(data=dfx, x='Pirmosios registracijos šalis', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo pirmosios registracijos šalies')
        axes.set(xlabel='Pirmosios registracijos šalis', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo TA galiojimo':
        dft['TA'] = dft['Tech. apžiūra iki'].apply(lambda x: int(x[:4]) if x != None else None)
        dft['Galioja_TA'] = dft['TA'].apply(lambda x: "Taip" if x > 2024 else 'Ne')
        dfx = dft.groupby(['Galioja_TA'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Galioja_TA', y='Kaina', ax=axes)
        axes.set_title('Kainos priklausomybė nuo TA galiojimo')
        axes.set(xlabel='Ar galioja TA?', ylabel='Kaina')

    elif selected_option == 'Populiariausi automobilių markės':
        dfx = dft.groupby(['Markė'])['Kaina'].count().reset_index().sort_values(by='Kaina', ascending=False)[:10]
        sns.barplot(data=dfx, x='Markė', y='Kaina', ax=axes)
        axes.set_title('Populiariausi automobilių markės')
        axes.set(xlabel='Markė', ylabel='Kiekis')

    for container in axes.containers:
        axes.bar_label(container)
    st.pyplot(fig)

# Parodyti grafiką pagal vartotojo pasirinkimą
show_chart(selected_option)
