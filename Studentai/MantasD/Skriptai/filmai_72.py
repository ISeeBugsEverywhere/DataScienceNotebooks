import streamlit as st
import pandas as pd
from datetime import datetime
from manofunkcijos import *
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
st.set_page_config(page_icon=':bar_chart', page_title='Filmo paieška', layout='wide')
st.title("Filmo paieška")
def metai(x):
    try:
        f = int(x.split('(')[1].replace(')',''))
        return int(f)
    except:
        return None
    
def find_user_top_genre(df):
    user_preferences = []
    for user_id, group in df.groupby('userId'):
        genre_totals = group.drop(columns=['userId', 'rating']).sum()
        top_genre = genre_totals.idxmax()  # Randa žanrą su didžiausia suma
        user_preferences.append({'userId': user_id, 'topGenre': top_genre})
    return pd.DataFrame(user_preferences)

links = pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/ml-32m/links.csv')
movies = pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/ml-32m/movies.csv')

moviesdf = movies['genres'].str.get_dummies('|')
mdf = pd.concat([movies, moviesdf], axis = 1)
movies_df = mdf.drop(columns=['genres','(no genres listed)'])

genres =  moviesdf.columns.tolist()[1:]

option1 = st.multiselect(
    "Žanrai:",
    options= genres)

filtered_movies_df = movies_df.copy()
df = filtered_movies_df
for number, option in enumerate(option1):
    df = filtered_movies_df if number == 0 else df
    filtered_movies_df = df
    df = filtered_movies_df[filtered_movies_df[option] == 1] if len(option1)>0 else filtered_movies_df
    
# st.dataframe(df)

atrinkti_filmai = list(df['movieId'].unique())
# st.text(atrinkti_filmai)
if len(option1) == 0:
  st.warning('Neparinktas nei vienas filmo žanras')
  st.stop()
st.success(f"Ačiū, tavo pasirinkti žanrai: {str(option1).replace('[','').replace(']','')}")

ratings = pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/ml-32m/ratings.csv')
ratings = ratings[ratings['movieId'].isin(atrinkti_filmai)]
ratings['datetime'] = ratings['timestamp'].apply(lambda x: datetime.fromtimestamp(x))

# Papildymas
# movies_ratings_full = pd.merge(left=ratings, right=movies_df, on='movieId')
# df = movies_ratings_full.drop(columns=['movieId','timestamp','datetime','title'])
# user_genre_df = find_user_top_genre(df)
db_path = '../../../../web_scrap.db'
query = 'SELECT * FROM user_genre_df;'  
user_genre_df = query_to_dataframe(db_path,query)
user_genre_df_filtered = user_genre_df[user_genre_df['topGenre'].isin(option1)]['userId'].tolist()
ratings = ratings[ratings['userId'].isin(user_genre_df_filtered)]
# 

datefrom = st.date_input('Nurodykite vertinimų pradžios datą', ratings['datetime'].min())
dateto = st.date_input('Nurodykite vertinimų pabaigos datą', ratings['datetime'].max())
ratings_filtered = ratings.query('datetime > @datefrom & datetime < @dateto')
ratings_group = ratings_filtered.groupby(['movieId'])['rating'].mean().reset_index()
# st.dataframe(ratings_group)
movies_ratings = pd.merge(left=movies_df, right=ratings_group, on='movieId')
movies_ratings['rating'] = movies_ratings['rating'].apply(lambda x: round(x,2))
# st.dataframe(movies_ratings)

rating_min, rating_max = st.slider(
    "Pasirinkite vertinimų intervalą",
    min_value=float(movies_ratings['rating'].min()),
    max_value=float(movies_ratings['rating'].max()),
    value=(float(movies_ratings['rating'].min()), float(movies_ratings['rating'].max()))
)


filtered_df = movies_ratings[(movies_ratings['rating'] >= rating_min) & (movies_ratings['rating'] <= rating_max)
]
atrinkti_filmai = list(filtered_df['movieId'].unique())
tags = pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/ml-32m/tags.csv')
tags = tags[tags['movieId'].isin(atrinkti_filmai)]
# st.dataframe(tags)
tags_df = tags
tags_df['tag'] = tags_df['tag'].apply(lambda x: str(x).lower())
tags_df = tags_df.groupby('movieId').apply(lambda x: '|'.join(x.tag)).reset_index()
tags_df['tags'] = tags_df[0]
tags_df = tags_df.drop(columns=0)
movies_ratings_tags = pd.merge(left=movies_ratings, right=tags_df, on='movieId')
movies_ratings_tags.dropna()
# st.dataframe(movies_ratings_tags)
text = st.text_input('Nurodykite ieškomą tekstą (autoriaus vardą, veikėją ar pan...)').lower()
# st.text(text)
movies_ratings_tags['Find_value'] = movies_ratings_tags['tags'].apply(lambda x: True if text in x else False)
po_filtravimo = movies_ratings_tags[movies_ratings_tags['Find_value'] == True][['title','rating']]
st.text('Rekomenduojami filmai:')
st.dataframe(po_filtravimo)
