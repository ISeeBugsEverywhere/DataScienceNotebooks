# Python bibliotekos
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

import streamlit as st

# Suppressing warnings
warnings.filterwarnings('ignore')   # Nustato, kad visi įspėjimai būtų ignoruojami

# Set up Selenium webdriver options
from selenium import webdriver                          # "selenium.webdriver" leidžia automatizuoti veiksmus interneto naršyklėje
from selenium.webdriver.chrome.options import Options   # "Options" leidžia nustatyti konfigūracijas Chrome naršyklės draiveriui

# Papildomai importuojame: 
from sklearn.linear_model import LinearRegression  # Tiesinės regresijos modelis
from sklearn.model_selection import train_test_split  # Duomenų padalijimas į treniravimo ir testavimo rinkinius
from sklearn.model_selection import train_test_split, cross_val_score

#Kreipiames i pagr. CSV
file_path = r'C:\Users\Pauliussl\Paskaita72\filmai\visi_filmai.csv'
df = pd.read_csv(file_path)
df = df.drop(columns=['timestamp_y','tmdbId','imdbId'])
df = df.drop(columns=['timestamp_x'])
df['genres_list'] = df['genres'].str.split('|')
df = df.drop(columns=['genres'])
df['tags'] = df.groupby('movieId')['tag'].transform(lambda x: ', '.join(x.dropna().unique()))
df['tags'] = df['tags'].astype(str)
df = df.drop(columns=['tag'])
df['title_count'] = df.groupby('title')['title'].transform('count')
df.rename(columns={'rating_avg': 'Rating'}, inplace=True)
# df['rating'] = df['rating'].astype(float)
df['Rating'] = df.groupby('title')['rating'].transform('mean')
df = df.drop(columns=['userId', 'rating'])
df = df.groupby('movieId', as_index=False).first()
df = df[df['title_count'] >= 500]

# Streamlit puslapio nustatymai 
st.set_page_config(layout="centered")  
st.title("Filmų žanras")

# Atrinkimo tipas 
all_options = {'Perziuriu skaicius', 'Auksciausias reitingas','Man vienodai'}
selected_options = st.selectbox("Pasirinkite vertinimo logika:", sorted(all_options))

# Filmu žanro pasirinkimai 
all_genres = {'Action', 'War', 'IMAX', 'Fantasy', 'Comedy', 'Mystery', 'Musical', 'Horror', 'Drama', 'Animation', 'Documentary', 'Children', 'Adventure', 'Thriller', 'Romance', 'Crime', 'Sci-Fi'}
selected_genre = st.selectbox("Pasirinkite žanrą:", sorted(all_genres))
selected_genre2 = st.selectbox("Pasirinkite žanrą 2:", sorted(all_genres))
filtered_df = df[df['genres_list'].apply(lambda genres: selected_genre in genres and selected_genre2 in genres)]   # Filtruojame duomenis pagal pasirinktą žanrą

# Filmu ratings pasirinkimai 
rating_selected = st.slider('Pasirinkite reitingą (nuo):', min_value=0, max_value=5, value=3)
filtered_df = filtered_df[filtered_df['Rating'] >= rating_selected]

# Tags pasirinkimai 
tag_selected = st.text_input("Iveskite zodi ar jo dali (tags paieska):", value="")
if tag_selected.strip():
    filtered_df = filtered_df[filtered_df['tags'].str.contains(tag_selected, case=False, na=False)]



# Sortinimo tipas pagal pasirinkta logika: 
if selected_options == 'Perziuriu skaicius':
    filtered_df = filtered_df.sort_values(by='title_count', ascending=False)
elif selected_options == 'Auksciausias reitingas':
    filtered_df = filtered_df.sort_values(by='Rating', ascending=False)
elif selected_options == 'Man vienodai':
    pass


st.subheader("Step 1: 7 geriausiai atitinkantys filmai")
wide_col = st.columns([1])[0]  # Sukuriame vieną stulpelį, kuris užima visą plotį
with wide_col:
    st.dataframe(filtered_df[['title', 'genres_list', 'Rating', 'title_count']].head(7), use_container_width=True)

st.subheader("Kiti nustatymai")

# TOP7 filmu pavadinimai 
st.subheader("Step 2: konkretus filmo pasirinkimas")
movie_titles = filtered_df['title'].head(7).tolist()
selected_movie = st.selectbox("Pasirinkite filmą iš sąrašo:", movie_titles)
st.write(f"Jūs pasirinkote filmą: **{selected_movie}**")


### Reitingu lenteles atvaizdavimas 
#Kreipiames i pagr. CSV
file_path = r'C:\Users\Pauliussl\Paskaita72\filmai\visi_filmai.csv'
df = pd.read_csv(file_path)
df = df.drop(columns=['timestamp_y','tmdbId','imdbId','movieId','genres', 'userId','timestamp_x', 'tag', 'timestamp_y'])
df['rating'] = df['rating'].round()
# Filtruojame duomenis pagal pasirinktą filmą
movie_data = df[df['title'] == selected_movie]
# Sukuriame reitingų dažnių lentelę pasirinktam filmui
rating_counts = movie_data['rating'].value_counts().sort_index(ascending=False)
# Stulpelių išdėstymas
col1, col2 = st.columns([1, 1])
# Diagramos rodymas kairėje pusėje
with col1:
    # Stulpelinė diagrama
    fig, ax = plt.subplots(figsize=(3, 3))  # Naudojame `fig, ax` struktūrą
    sns.barplot(y=rating_counts.index, x=rating_counts.values, palette="viridis", orient='h', ax=ax)
    ax.set_ylabel('Reitingas', fontsize=14)
    ax.set_yticks(rating_counts.index)
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Diagramos rodymas dešinėje pusėje
with col2:
    # Skritulinė diagrama
    fig, ax = plt.subplots(figsize=(3, 3))  # Naudojame `fig, ax` struktūrą
    ax.pie(
        rating_counts.values, 
        labels=rating_counts.index, 
        autopct='%1.1f%%',  # Parodoma procentinė dalis
        startangle=140,  # Sukamės, kad pradėtume nuo kito kampo
        colors=sns.color_palette("viridis", len(rating_counts))  # Naudojame "viridis" spalvų paletę
    )
    ax.set_title('Reitingų pasiskirstymas', fontsize=14)
    st.pyplot(fig)







