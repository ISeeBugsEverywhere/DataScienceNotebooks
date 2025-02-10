import streamlit as st
import pandas as pd

movies_path = r"C:\Users\Batia\Downloads\ml-32m\ml-32m\movies.csv"
ratings_path_1 = r"C:\Users\Batia\Downloads\ml-32m\ml-32m\ratings.csv"

movies_df = pd.read_csv(movies_path)
ratings_df_1 = pd.read_csv(ratings_path_1)

# Soedinenie dvuh tablic
merged_df = pd.merge(ratings_df_1, movies_df, on="movieId", how="inner")

# Izvle4enie goda iz nazvanija
merged_df['year'] = merged_df['title'].str.extract(r'\((\d{4})\)').astype(float)

# Streamlit
def main():
    st.title("Movie Recommendations")

    # Filtry
    st.sidebar.header("Filters")

    # janrovye filtry
    unique_genres = set(
        genre for sublist in merged_df['genres'].str.split('|') for genre in sublist
    )
    genres_selected = st.sidebar.multiselect("Select Genres", sorted(unique_genres))

    # filtr minimalnogo rejtinga
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0, step=0.5)

    # filtr godovogo promezutka
    min_year = int(merged_df['year'].min())
    max_year = int(merged_df['year'].max())
    year_range = st.sidebar.slider("Year Range", min_year, max_year, (1990, 2000))

    # Filtrujet filmy isxodia iz vvodimogo userom
    def filter_movies(df, genres=None, min_rating=None, year_range=None):
        filtered_df = df.copy()

        # Filtr janra
        if genres:
            genre_filter = filtered_df['genres'].apply(
                lambda x: any(genre in x for genre in genres)
            )
            filtered_df = filtered_df[genre_filter]

        # Filtr minimalnogo rejtinga
        if min_rating:
            filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

        # Filtr godovogo promezutka
        if year_range:
            start_year, end_year = year_range
            filtered_df = filtered_df[
                (filtered_df['year'] >= start_year) & (filtered_df['year'] <= end_year)
            ]


        # Sniat duplikaty
        filtered_df = filtered_df.drop_duplicates(subset=['title', 'genres'])

        return filtered_df

    # Priminenie filtrov
    filtered_movies = filter_movies(
        merged_df, genres=genres_selected, min_rating=min_rating, year_range=year_range
    )

    # Pokaz rezultatov s limitom
    st.subheader("Recommended Movies")
    filtered_display = filtered_movies[
        ["title", "genres", "rating", "year"]
    ].sort_values(by="rating", ascending=False)

    # tolko top 100 stro4ek
    st.write(filtered_display.head(100))

if __name__ == "__main__":
    main()