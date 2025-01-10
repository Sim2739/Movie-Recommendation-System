import streamlit as st
import pickle
import requests
import pandas as pd
import numpy as np

st.title('Movie Recommendation System')

# Load movies list and similarity matrix
movies_list = pickle.load(open('movies.pkl', 'rb'))  # Assuming this is a DataFrame
similarity = pickle.load(open('movie_recommendation_system.pkl', 'rb'))

# Function to fetch movie poster URL from TMDB API (Not used here, but kept for reference)
def fetch_poster(movie_id):
    api_key = '3a6cabea5954a272326ecf07bbeea3f4'  # Replace with your actual TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f'https://image.tmdb.org/t/p/w500{poster_path}'
        return full_path
    else:
        return None

# Function to recommend movies
def recommend(movie, similarity_matrix, movies_df):
    try:
        # Check if the movie exists in the dataset
        if movie not in movies_df['original_title'].values:
            return ["Movie not found in the dataset."]
        
        # Find the index of the selected movie
        movie_index = movies_df[movies_df['original_title'] == movie].index[0]
        
        # Calculate similarity scores
        similarity_score = list(enumerate(similarity_matrix[movie_index]))
        
        # Sort movies by similarity score
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        
        # Fetch top 10 similar movies (excluding the first one)
        recommended_movies = []
        recommended_movies_posters = []
        for i in sorted_similar_movies[1:11]:  # Skip the first one (the same movie)
            movie_id = movies_df.iloc[i[0]].id
            title = movies_df.iloc[i[0]].original_title
            poster_url = fetch_poster(movie_id)
            recommended_movies.append(title)
            recommended_movies_posters.append(poster_url)
        
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        return [], []

# Select box for movie input
selected_movie_name = st.selectbox(
    'Enter your favorite movie!', 
    movies_list['original_title'].values,
    key='movie_selectbox'
)


# Button to trigger recommendation
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, similarity, movies_list)

    if names:
        st.write("Movies suggested for you:")
        cols = st.columns(5)  # Create 5 columns for displaying movies and posters
        for idx, col in enumerate(cols[:len(names)]):
            with col:
                st.text(names[idx])
                if idx < len(posters) and posters[idx]:
                    st.image(posters[idx], use_container_width=True)
                else:
                    st.text("Poster unavailable.")
    else:
        st.write("No recommendations found.")
