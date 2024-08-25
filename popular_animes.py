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

def app():
    popular_dict = pickle.load(open('popular_dict.pkl', 'rb'))
    popular = pd.DataFrame(popular_dict)

    st.title('Anime :red[Recomannia] by :red[Rishabh] :sunglasses:')
    st.header(":red[Popular] Animes", divider="red")

    popular_id_list = popular['anime_id'].values

    # Fetch all anime information at once, then display
    valid_anime_list = [fetch_anime_info(anime_id) for anime_id in popular_id_list if fetch_anime_info(anime_id)]

    columns_per_row = 4
    for i in range(0, len(valid_anime_list), columns_per_row):
        cols = st.columns(columns_per_row)

        for j, col in enumerate(cols):
            index = i + j
            if index < len(valid_anime_list):
                anime_info = valid_anime_list[index]
                with col:
                    st.image(anime_info['images']['jpg']['image_url'], use_column_width=True)
                    st.markdown(f"**{anime_info['title']}**")
                    st.markdown(f"⭐ {anime_info['score']} | 🎬 {anime_info['type']}")

                    genres = [genre['name'] for genre in anime_info.get('genres', [])]
                    genre_text = ', '.join(genres) if genres else 'N/A'
                    st.markdown(f"🏷 {genre_text}")

    st.header("", divider="red")



