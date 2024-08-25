import streamlit as st
import popular_animes
import recommendation

pages = {
    "Popular Animes": popular_animes,
    "Recommendation": recommendation
}

st.sidebar.title("Pages")
selection = st.sidebar.radio("Go to", list(pages.keys()))

page = pages[selection]
page.app()
