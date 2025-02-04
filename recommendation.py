import streamlit as st
import pickle
import pandas as pd
import requests
from functools import lru_cache

@lru_cache(maxsize=1000)
def fetch_anime_info(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('data', {})
        if data.get('images') and data.get('title') and data.get('score') is not None:
            return data
    return None

def recommend_based_on_content(anime_name, anime, cosine_sim):
    idx = anime[anime['name'] == anime_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    anime_indices = [i[0] for i in sim_scores]
    recommended_animes = []
    recommended_anime_info = []
    for i in anime_indices:
        anime_id = anime['anime_id'].iloc[i]
        recommended_animes.append(anime['name'].iloc[i])
        anime_info = fetch_anime_info(anime_id)
        if anime_info:
            recommended_anime_info.append(anime_info)
    return recommended_animes, recommended_anime_info



def app():
    anime_dict = pickle.load(open('anime.pkl', 'rb'))
    anime = pd.DataFrame(anime_dict)
    cosine_sim = pickle.load(open('similarity.pkl', 'rb'))

    st.title('Anime :red[Recomannia] by :red[Rishabh] :sunglasses:')

    selected_anime_name = st.selectbox('Choose an Anime for similar recommendations', anime['name'].values)

    if st.button('Recommend'):
        content_based_recommendations, content_based_reco_info = recommend_based_on_content(
            selected_anime_name, anime, cosine_sim)

        st.header("Content Based Recommendations", divider="red")
        columns_per_row = 5
        for i in range(0, len(content_based_recommendations), columns_per_row):
            cols = st.columns(columns_per_row)
            for j, col in enumerate(cols):
                index = i + j
                if index < len(content_based_reco_info):  # Check if the index is within bounds
                    anime_info = content_based_reco_info[index]
                    with col:
                        st.image(anime_info['images']['jpg']['image_url'], use_container_width=True)
                        st.markdown(f"**{anime_info['title']}**")
                        st.markdown(f"⭐ {anime_info['score']} | 🎬 {anime_info['type']}")
                        genres = [genre['name'] for genre in anime_info.get('genres', [])]
                        genre_text = ', '.join(genres) if genres else 'N/A'
                        st.markdown(f"🏷 {genre_text}")
                else:
                    break  # Stop if we run out of recommendations
        st.header("", divider="red")
