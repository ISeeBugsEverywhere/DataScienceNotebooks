import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')



@st.cache_data
def load_and_combine_data():    


    ratings = pd.read_csv('../../../eismas/ml-32m/ratings.csv')

    # def convert_timestamp_to_datetime(x):
    #     dt_object = datetime.fromtimestamp(x)
    #     return dt_object

    # ratings['datetime'] = ratings['timestamp'].apply(convert_timestamp_to_datetime)

    # vidurkinam ratinga
    ratings_gr1 = ratings.groupby('movieId').agg(
        rating_mean=('rating', 'mean'),
        rating_count=('rating', 'count')
        # timestamp=('timestamp', 'min'),
        # datetime=('datetime', 'min')
    ).reset_index()

    ratings_gr1['rating_mean'] = ratings_gr1['rating_mean'].round(2)

    movies = pd.read_csv('../../../eismas/ml-32m/movies.csv')
    tags = pd.read_csv('../../../eismas/ml-32m/tags.csv')
    # Group by movieid and aggregate tags into a list
    movie_tags_df = tags.groupby('movieId')['tag'].apply(list).reset_index()
    # Rename columns for clarity
    movie_tags_df.columns = ['movieId', 'tags']
    # Merge the DataFrames on 'movieId'
    merged_df = pd.merge(ratings_gr1, movie_tags_df, on='movieId', how='inner')
    combined_movies = pd.merge(merged_df, movies, on='movieId', how='inner')
    return combined_movies

moviesdf = load_and_combine_data()

# unique tags and genres
unique_tags = list(set(tag for tags in moviesdf['tags'] for tag in tags))
all_genres = moviesdf['genres'].str.split('|').explode().unique()
unique_genres = list(all_genres)

st.write('Data prepared')

# Pasirinkimai
min_rating, max_rating = st.slider(
    'Select Rating Range',
    min_value=0.0,
    max_value=5.0,
    value=(1.0, 4.5),  # Default range
    step=0.5
)

selected_genre = st.multiselect('Select movie genre:', unique_genres)
selected_tag= st.multiselect('Select movie tag:', unique_tags)


# Create a button in Streamlit
if st.button('Ieškoti'):
    # kai nuspaudžiamas mygtukas
    st.write(f"Selected genres: {selected_genre}")
    st.write(f"selected tags: {selected_tag}")

    genres_to_filter = selected_genre

    # Filter movies that have all genres in the genres column
    movies_by_genre = moviesdf[moviesdf['genres'].apply(lambda x: all(genre in x for genre in genres_to_filter))]

    tags_to_filter = selected_tag
    movies_by_tags = movies_by_genre[movies_by_genre['tags'].apply(lambda tags: any(tag in tags for tag in tags_to_filter))]

    st.dataframe(movies_by_tags)

