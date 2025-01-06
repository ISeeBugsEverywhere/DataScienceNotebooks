import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

import warnings
warnings.filterwarnings('ignore')

import streamlit as st

st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='wide')

@st.cache_data
def pirma():
    df_movies = pd.read_csv(r"C:\Users\pauli\Downloads\ml-32m\movies.csv")
    df_ratings = pd.read_csv(r"C:\Users\pauli\Downloads\ml-32m\ratings.csv")
    df_tags = pd.read_csv(r"C:\Users\pauli\Downloads\ml-32m\tags.csv")

    df_ratings1 = df_ratings.groupby('movieId').agg(
        mean_rating=('rating', 'mean'),
        rating_count=('rating', 'count')
    )
    df_bendras = pd.merge(df_movies, df_ratings1, on='movieId', how='left')
    df_tags1 = df_tags.groupby(['movieId'])['tag'].apply(lambda x: '|'.join(map(str, x))).reset_index()
    df_tags1['tag'] = df_tags1['tag'].str.lower()
    df_bendras = pd.merge(df_bendras, df_tags1, on='movieId', how='left')
    return df_bendras

@st.cache_data
def antra():
    df_movies = pd.read_csv(r"C:\Users\pauli\Downloads\ml-32m\movies.csv")
    df_ratings = pd.read_csv(r"C:\Users\pauli\Downloads\ml-32m\ratings.csv")

    dfM = pd.merge(df_ratings, df_movies, on='movieId', how='left')
    return dfM

dftest = pirma()

dfM = antra()

zanrai = ["Nieko", "Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    
selected_genres = []
for i in range(3):
    genre = st.selectbox(f'Pasirinkite filmo žanrą {i + 1}:', zanrai)
    if genre != 'Nieko':
        selected_genres.append(genre)
for genre in selected_genres:
    dftest = dftest[dftest['genres'].str.contains(genre, na=False)]


min_val, max_val = st.slider('Pasirinkite filmų reitingo intervalą:', min_value=0.0, max_value=5.0, value=(2.0, 5.0), step=0.1)
dftest = dftest[dftest['mean_rating'].between(min_val, max_val, inclusive='both')]

max_balsu = int(dftest['rating_count'].max())
min_val, max_val = st.slider('Pasirinkite, kiek žmonių turėtų būti pateikę savo filmo vertinimą', min_value=1, max_value=max_balsu, value=(1, max_balsu), step=1)
dftest = dftest[dftest['rating_count'].between(min_val, max_val, inclusive='both')]

dftest = dftest.sort_values('mean_rating', ascending=False).reset_index()
dftest.drop('index', axis=1, inplace=True)
dftest.drop('movieId', axis=1, inplace=True)
st.write(dftest.head(1000))

st.write('antras, Mykolo,variantas')

zanrai = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

genre = st.selectbox(f'Pasirinkite filmo žanrą:', zanrai)
dfM = dfM[dfM['genres'].str.contains(genre, na=False)]

dfM2 = dfM.groupby('userId')['genres'].count().reset_index()
dfM2.rename(columns={'genres': 'balsiukai'}, inplace=True)

dfM = pd.merge(dfM, dfM2, on='userId', how='left')

number = st.number_input(
    label="nuo kiek balsų priimsime vertinitojus?",
    min_value=0,
    max_value=2000,
    value=30,
    step=1
)
dfM  = dfM [dfM ['balsiukai'] >= number]

dfMr = dfM.groupby('movieId').agg(
    mean_rating=('rating', 'mean'),
    rating_count=('rating', 'count')
)
dfM1 = dfM[['movieId', 'title']]

max_balsu = int(dfMr['rating_count'].max())
min_val, max_val = st.slider('Pasirinkite, kiek žmonių turėtų būti pateikę savo filmo vertinimą', min_value=1, max_value=max_balsu, value=(1, max_balsu), step=1)
dfMr = dfMr[dfMr['rating_count'].between(min_val, max_val, inclusive='both')]
dfMr =  pd.merge(dfMr, dfM1, on='movieId', how='left')
dfMr = dfMr.drop_duplicates()
dfMr = dfMr.sort_values('mean_rating', ascending=False).reset_index()
# dfMr = dfMr.drop(['movieId','userId', 'balsiukai', 'index', 'rating', 'timestamp'], axis=1)
st.write(dfMr.head(1000))